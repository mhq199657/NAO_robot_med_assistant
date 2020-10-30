#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: A Simple class to get & read FaceDetected Events"""

import qi
import time
import sys
import argparse
import os
import csv
import wave
import contextlib


class VoiceRecorder(object):
    """
    A simple class to react to sound detection events.
    """

    def __init__(self, app):
        """
        Initialisation of qi framework and event detection.
        """
        super(VoiceRecorder, self).__init__()
        app.start()
        session = app.session
        # Get the service ALMemory.
        self.memory = session.service("ALMemory")
        # Connect the event callback.
        self.subscriber = self.memory.subscriber("SoundDetected")
        self.subscriber.signal.connect(self.on_sound_detected)
        # Get the services ALTextToSpeech, ALAudioRecorder and ALSoundDetection.
        self.tts = session.service("ALTextToSpeech")
        self.record = session.service("ALAudioRecorder")
        self.sound_detection = session.service("ALSoundDetection")
        self.sound_detection.subscribe("VoiceRecorder")
        self.got_sound = False

    def on_sound_detected(self, value):
        """
        Callback for event SoundDetected.
        """
        if value == []:  # empty value when the face disappears
            self.got_sound = False
        elif not self.got_sound:  # only speak the first time a face appears
            self.got_sound = True

            print "sound detected"
            print "value:", value
            self.record.stopMicrophonesRecording()
            print 'start recording...'
            record_path = '/home/nao/yiyang/on_event_record.wav'
            self.record.startMicrophonesRecording(record_path, "wav", 16000, (0, 0, 1, 0))
            current_timestamp = time.time()
            readable_timestamp = time.ctime(current_timestamp)
            time.sleep(5)
            self.record.stopMicrophonesRecording()
            print 'record over'

            print 'start detecting your emotion'
            cwd = os.getcwd()
            if cwd == "/data/home/nao/yiyang/openEAR-0.1.0":
                print "in the correct directory"
            else:
                os.chdir("openEAR-0.1.0")
                print "cwd changed to:", os.getcwd()

            config = "config/emobase_print_emotion.conf"
            os.system("./SMILExtract -C %s -I %s -O output.arff" % (config, record_path))
            cwd = os.getcwd()
            log_file_path = os.path.join(cwd, "smile.log")
            emo_record_path = '/home/nao/yiyang/on_speech_detected.csv'

            with contextlib.closing(wave.open(record_path, 'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = frames / float(rate)

            with open(log_file_path, "r") as file:
                # model trained on EmoDB
                emotionClassification = ''
                for line in file:
                    if line.startswith(" LibSVM  'emodbEmotion' result"):
                        tokens = line.split()
                        for i in range(len(tokens)):
                            if tokens[i] == '~~>':
                                emotionClassification = tokens[i + 1]
                                with open(emo_record_path, 'a') as csvfile:
                                    emo_record_writer = csv.writer(csvfile, delimiter=' ',
                                                                   quotechar=" ", quoting=csv.QUOTE_MINIMAL)
                                    fields = (emotionClassification, str(readable_timestamp), str(duration))
                                    emo_record_writer.writerow(fields)
                                break
                        break
            print 'Timestamp:', current_timestamp
            print 'Emotion Recognition Result:', emotionClassification
            print 'Duration:', duration
            os.remove(record_path)

    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print "Starting VoiceRecorder"
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print "Interrupted by user, stopping VoiceRecorder"
            self.sound_detection.unsubscribe("VoiceRecorder")
            #stop
            sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["VoiceRecorder", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    voice_recorder = VoiceRecorder(app)
    voice_recorder.run()
