from naoqi import ALProxy
import time
import os
import csv
import wave
import contextlib

robot_IP = "192.168.121.175"
robot_PORT = 9559
tts = audio = record = aup = None

tts = ALProxy("ALTextToSpeech", robot_IP, robot_PORT)
record = ALProxy("ALAudioRecorder", robot_IP, robot_PORT)

record.stopMicrophonesRecording()
print 'start recording...'
tts.say("hi I am nao robot.")
tts.say("start recording...")
record_path = '/home/nao/yiyang/test_record.wav'
record.startMicrophonesRecording(record_path, "wav", 16000, (0, 0, 1, 0))
current_timestamp = time.time()
readable_timestamp = time.ctime(current_timestamp)
time.sleep(5)
record.stopMicrophonesRecording()
print 'record over'
tts.say("record over")

tts.say("start detecting your emotion")
os.chdir("openEAR-0.1.0")
print 'change cwd to', os.getcwd()
config = "config/emobase_print_emotion.conf"
os.system("./SMILExtract -C %s -I %s -O output.arff" % (config, record_path))
cwd = os.getcwd()
log_file_path = os.path.join(cwd, "smile.log")
emo_record_path = '/home/nao/yiyang/emo_record.csv'
with open(emo_record_path, 'a') as csvfile:
    emo_record_writer = csv.writer(csvfile, delimiter=' ',
                                   quotechar='|', quoting=csv.QUOTE_MINIMAL)
    emo_record_writer.writerow(('Emotion', 'Timestamp', 'Duration'))

with contextlib.closing(wave.open(record_path,'r')) as f:
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
                    print 'Timestamp:', current_timestamp
                    print 'Emotion Recognition Result:', emotionClassification
                    print 'Duration:', duration
                    tts.say("Your emotion is %s" % emotionClassification)
                    with open(emo_record_path, 'a') as csvfile:
                        emo_record_writer = csv.writer(csvfile, delimiter=' ',
                                                quotechar=" ", quoting=csv.QUOTE_MINIMAL)
                        fields = (emotionClassification, str(readable_timestamp), str(duration))
                        emo_record_writer.writerow(fields)
                    break
            break
    os.remove(record_path)

