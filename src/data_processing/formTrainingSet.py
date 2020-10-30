import sys
import os
import random
from shutil import copyfile

if __name__ == '__main__':
    cwd = os.getcwd()
    originDir = os.path.join(cwd, "10_Partitions_Shuffle")
    if not os.path.exists(originDir):
        exit("directory for dataset not found")

    k = 10;

    for validationSet in range(1, k + 1):
        outputDir = os.path.join(cwd, "kFoldTrainingSet", "TrainingSetWithout" + str(validationSet))

        if os.path.exists(outputDir):
            for root, dirs, files in os.walk(outputDir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
            for root, dirs, files in os.walk(outputDir, topdown=False):
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(outputDir)
            print(outputDir + ' is removed.')

        os.mkdir(outputDir)
        emotions = {
            "N": "Neutral",
            "W": "Angry",
            "L": "Boredom",
            "E": "Disgust",
            "A": "Fear",
            "F": "Happy",
            "T": "Sad"
        }

        for emotion in emotions:
            emotionDir = os.path.join(outputDir, emotions[emotion])
            os.mkdir(emotionDir)

        count = 0
        for i in range(1, k + 1):
            if i == validationSet:
                continue
            partitionDir = os.path.join(originDir, str(i))
            for emotion in emotions:
                emotionDir = os.path.join(partitionDir, emotions[emotion])
                for root, dirs, files in os.walk(emotionDir):
                    for file in files:
                        src = os.path.join(emotionDir, file)
                        dst = os.path.join(outputDir, emotions[emotion], file)
                        copyfile(src, dst)
                        count = count + 1

        print(count, "files are copied to new directory in total")
