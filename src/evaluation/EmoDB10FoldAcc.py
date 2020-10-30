import sys
import os
from shutil import copyfile

if __name__ == '__main__':
    cwd = os.getcwd()
    dataset = os.path.join(cwd, "10_Partitions_Shuffle", "Person16")

    emotions = {
        "N": "Neutral",
        "W": "Angry",
        "L": "Boredom",
        "E": "Disgust",
        "A": "Fear",
        "F": "Happy",
        "T": "Sad"
    }

    total = 0
    counted = 0
    matched = 0
    for root, dirs, files in os.walk(dataset):
        for file in files:
            if not file.startswith('.'):
                total = total + 1
                splitted = file.split(".")
                characters = list(splitted[0])
                extension = splitted[1]
                emotion = emotions[characters[5]]
                print("!!!!!!!!!emotion:", emotion)

                input = os.path.join(root, file)
                os.system("cd ")
                os.system("SMILExtract -C config/emo_large.conf -I %s -O output.arff" % input)
                log_file_path = os.path.join(cwd, "smile.log")
                with open(log_file_path, "r") as file:
                    # model trained on EmoDB
                    emotionClassification = ''
                    for line in file:
                        if line.startswith(" LibSVM  'emodbTrain' result"):
                            tokens = line.split()
                            for i in range(len(tokens)):
                                if tokens[i] == '~~>':
                                    emotionClassification = tokens[i + 1]
                                    counted = counted + 1
                                    break
                            break
                    if emotionClassification == emotion:
                        matched = matched + 1

    print("Evaluated on EmoDB evaluation set", total)
    print("------------evaluate EmoDB Model on its evaluation set-----------")
    print("counted", counted)
    print("matched", matched)









