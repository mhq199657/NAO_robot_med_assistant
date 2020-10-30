import sys
import os
import random
from shutil import copyfile

if __name__ == '__main__':
    cwd = os.getcwd()
    originDir = os.path.join(cwd, "wav")
    if not os.path.exists(originDir):
        exit("directory for dataset not found")
    outputDir = os.path.join(cwd, "10_Partitions_Shuffle")
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

    Nlist = [];
    Wlist = [];
    Llist = [];
    Elist = [];
    Alist = [];
    Flist = [];
    Tlist = [];
    emotionLists = {
        "N": Nlist,
        "W": Wlist,
        "L": Llist,
        "E": Elist,
        "A": Alist,
        "F": Flist,
        "T": Tlist
    }

    k = 10;

    for i in range(1, k + 1):
        partitionDir = os.path.join(outputDir, str(i))
        os.mkdir(partitionDir)
        for emotion in emotions:
            emotionDir = os.path.join(partitionDir, emotions[emotion])
            os.mkdir(emotionDir)
            
    for root, dirs, files in os.walk(originDir):
        for file in files:
            if not file.startswith('.'):
                splitted = file.split(".")
                characters = list(splitted[0])
                emotion = characters[5]
                emotionLists[emotion].append(file)

    for emotion in emotionLists:
        print("emotion:", emotion, "length:", len(emotionLists[emotion]))
        random.shuffle(emotionLists[emotion])

    count = 0
    for emotion in emotionLists:
        part = 0
        emoList = emotionLists[emotion]
        for emoFile in emoList:
            src = os.path.join(originDir, emoFile)
            dst = os.path.join(outputDir, str(part % 10 + 1), emotions[emotion], emoFile)
            copyfile(src, dst)
            count = count + 1
            part = part + 1

    print(count, "files are copied to new directory in total")
