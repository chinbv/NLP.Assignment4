# -*- coding: utf-8 -*-
##############################################################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################
#####
##### Brandon Chin
##### Monday, March 18th, 2019
##### CMSC 416 - Natural Language Processing
##### Programming Assignment 3 - POS Tagger
#####
##### 1. The Problem
##### Write a perl (or python3) program called tagger.(pl|py) which will take as input a training file containing part of speech tagged text, and a file containing text to be part of speech tagged.
#####
##### 2. Example Input/Output
#####
##### [Input] python tagger.py pos-train.txt pos-test.txt >  pos-test-with-tags.txt
#####
##### [pos-train.txt] [ Pierre/NNP Vinken/NNP ]
##### [pos-train.txt] ,/,
##### [pos-train.txt] [ 61/CD years/NNS ]
##### [pos-train.txt] old/JJ ,/, will/MD join/VB
##### [pos-train.txt] [ the/DT board/NN ]
#####
##### [pos-test.txt] No ,
##### [pos-test.txt] [ it ]
##### [pos-test.txt] [ was n't Black Monday ]
##### [pos-test.txt] .
##### [pos-test.txt] But while
##### [pos-test.txt] [ the New York Stock Exchange ]
#####
##### [pos-test-with-tags.txt] No/NNP
##### [pos-test-with-tags.txt] ,/,
##### [pos-test-with-tags.txt] [ it/PRP
##### [pos-test-with-tags.txt] ]
##### [pos-test-with-tags.txt] [ was/VBD
##### [pos-test-with-tags.txt] n't/RB
##### [pos-test-with-tags.txt] Black/NNP
##### [pos-test-with-tags.txt] Monday/NNP
##### [pos-test-with-tags.txt] ]
##### [pos-test-with-tags.txt] ./.
#####
##### [Input] python scorer.py pos-test-with-tags.txt pos-test-key.txt
#####
##### [pos-test-key.txt] No/RB ,/,
##### [pos-test-key.txt] [ it/PRP ]
##### [pos-test-key.txt] [ was/VBD n't/RB Black/NNP Monday/NNP ]
##### [pos-test-key.txt] ./.
##### [pos-test-key.txt] But/CC while/IN
##### [pos-test-key.txt] [ the/DT New/NNP York/NNP Stock/NNP Exchange/NNP ]
##### [pos-test-key.txt] did/VBD n't/RB
#####
##### [Output] 85.6997043503% CORRECT
##### [Output] 14.3002956497% INCORRECT
##### [Output] JJ|IN NNP 1
##### [Output] RP$ PRP$ 491
##### [Output] PRP$ NNP 19
##### [Output] VBG JJ 2
##### [Output] VBG NN 261
##### [Output] VBG NNP 31
##### [Output] VBD VB 10
##### [Output] VBD NN 142
##### [Output] VBD VBD 1460
##### [Output] VBD VBN 218
##### [Output] VBD JJ 4
##### [Output] VBD NNP 3
#####
##### 3. Algorithm
#####
##### #1. Read the arguments from the command line to in order to build a dictionary (train) of words and possible POS in the tagger.py
#####
##### #2. With the dictionary of words and possible parts of speeches, read the test file to then output to a new file the words with the most frequent
#####     part of speech found in the dictionary. If there are any additional rules for tagging a word with a part of speech, it will be used here
#####
##### #3. With this new file that has the words from the test file with the tagger.py assigned parts of speech, the scorer.py will compare this file to the key.
#####     The key will return the percentage of correctly guessed parts of speeches when comparing the two files, as well as the confusion matrix
#####
##############################################################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################

## with training you order the features by most distinguishing
## then run through array against the test data
## but the training data needs to be scored as well
##
##
##
##
##



import re
import sys
from decimal import Decimal
from random import *
import operator


def main():##main method

    # print("This program tags words with POS.")
    # print("Created by Brandon Chin")

    numberOfArgs = len(sys.argv)
    # print "there are " + str(numberOfArgs) + " arguments"
    # if numberOfArgs < 3:
    #     # print "Usage: " + sys.argv[0] + " n m <filenames> where n = number of grams, m = number of sentences"
    #     exit(1)

    # trainingData = sys.argv[1]
    # testData = sys.argv[2]
    numberOfArgs -= 1 # adjust
    argsIndex = 1
    aboutToCollectContents = False
    senseIdTag = None
    # senseId = None
    totalCount = 0
    trainedSenseId = None

    while argsIndex <= numberOfArgs:
        loadFileName = sys.argv[argsIndex]
        f = open(loadFileName,"r")
        contents = f.readlines()
        f.close()
        if argsIndex == 1:
            for line in contents:
                if aboutToCollectContents == True:
                    # print ("line is: " + str(line))
                    if generate_tokens(line) == "phone":
                        senseIdTag = "phone"
                    else:
                        senseIdTag = "product"
                    print ("senseid=" + str(senseIdTag))
                    aboutToCollectContents = False
                    # print ("contextLine: " + str(contextLine))
                    # if contextLine != "</context>":
                    # print ("contextLine: " + str(contextLine))
                    # newSenseId = feature1(contextLine)
                    # print ("newSenseId: " + str(newSenseId))
                if "<answer" in line:
                    answerLine = line
                    totalCount += 1

                    phonePattern = re.compile(r'\bphone\b')
                    phoneMatch = phonePattern.match(''.join(answerLine))
                    # print "cardinalMatch " + str(cardinalMatch)
                    phoneToken = None
                    if phoneMatch != None:
                        phoneToken = phoneMatch.group()

                    print ("phoneToken: " + str(phoneToken))

                    print ("answerLine: " + answerLine)
                if "<context>" in line:
                    aboutToCollectContents = True
                # if "</context>" in line:
                #     aboutToCollectContents = False
            for l in range(len(frequencyArray)):
                # print ("length is " + str(len(frequencyArray)))
                # beautify = frequencyArray.join(frequencyArray[l])
                # print ("[" + frequencyArray[l] + "]")

                # print (frequencyArray[l], end=" ")
                print(str(frequencyArray[l]) + " ", end='')

                # print ("frequencyArray " + str(frequencyArray[l]) + ",")

            print ("TotalCount= " + str(totalCount))
        if argsIndex == 2:
            print ("\n I got here [2]")
        argsIndex += 1


def feature1(contextLine):
    senseId = None
    if "phone" in contextLine:
        senseId = "phone"
    # else:
    #     print ("Does not contain phone")

    return senseId

def feature2(contextLine):
    senseId = None
    if "call" in contextLine:
        senseId = "phone"
    # else:
    #     print ("Does not contain call")

    return senseId

def feature3(contextLine):
    senseId = None
    if "telephone" in contextLine:
        senseId = "phone"
    # else:
    #     print ("Does not contain telephone")

    return senseId

def feature4(contextLine):
    senseId = None
    if "tele" in contextLine:
        senseId = "phone"
    # else:
    #     print ("Does not contain tele")

    return senseId

def feature5(contextLine):
    senseId = None
    if "number" in contextLine:
        senseId = "phone"
    # else:
    #     print ("Does not contain number")

    return senseId

arrayOfFunctions = [feature1, feature2, feature3, feature4, feature5]

freq1 = 0
freq2 = 0
freq3 = 0
freq4 = 0
freq5 = 0

frequencyArray = [freq1,freq2,freq3,freq4,freq5]

#Dealing with the test file tokens
def generate_tokens(s):

    resultingSenseId = None
    # s = re.sub("[\[\]]", '', s)

    # Replace new lines with spaces
    s = re.sub(r'\s+', ' ', s)

    # Break sentence into the tokens, remove empty tokens
    tokens = [token for token in s.split(" ") if token != ""]

    # print ("Token is: " + str(tokens) + "\n")


    count = 0

    for i in range(len(arrayOfFunctions)):
        f = arrayOfFunctions[i]
        # print ("f=" + str(f))

        resultingSenseId = f(tokens)

        if resultingSenseId == "phone":
            index = i
            print ("index is: " + str(index))
            frequencyArray[index] += 1

            print("frequencyArray " + str(frequencyArray[index]))

        print ("resultingSenseId is: " + str(resultingSenseId))

        # print ("resultingSenseId is: " + str(resultingSenseId) + " count " + str(count))

        # count += 1
        # print ("Count is: " + str(count))

    return resultingSenseId



if __name__ == "__main__":
    main()
