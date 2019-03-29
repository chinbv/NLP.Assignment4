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

### Rules and Accuracy
##
## 1. With no additional rules except for most frequent pos
# 84.4396733774% CORRECT
# 15.5603266226% INCORRECT
## 2. Any capital letter means a POS with NNP, and then most frequent pos
# 85.6997043503% CORRECT
# 14.3002956497% INCORRECT
## 3. Any number that is read in is classified as CD, and then most frequent pos
# 85.1981557089% CORRECT
# 14.8018442911% INCORRECT
## 4. Any word that ends in -ly is classified as RB, and then most frequent pos
# 83.3538645643% CORRECT
# 16.6461354357% INCORRECT
## 5. Any word that begins with un- or Un- is classified as JJ, and then most frequent pos
# 83.3186681684% CORRECT
# 16.6813318316% INCORRECT
## 6. Any word that begins with in- or In- is classified as JJ, and then most frequent pos
# 78.6956215684% CORRECT
# 21.3043784316% INCORRECT
## 6. Combination of all the rules
# 79.4470646206% CORRECT
# 20.5529353794% INCORRECT

import re
import sys
from decimal import Decimal
from random import *
import operator
from fractions import Fraction

keyTokenDict = {}

def main():##main method

    # print("This program tags words with POS.")
    # print("Created by Brandon Chin")

    numberOfArgs = len(sys.argv)
    numberOfArgs -= 1 # adjust
    argsIndex = 1
    fTestFile = None
    fKeyFile = None

    # while argsIndex <= numberOfArgs:
    #     loadFileName = sys.argv[argsIndex]
    #     # print "opening file " + loadFileName
    #     # f = open(loadFileName,"r")
    #     # contents = f.read()
    #     # f.close()
    #     # print contents + "\n"
    #     fTestFile = sys.argv[1]
    #     fKeyFile = sys.argv[2]
    #     print "fTestFile: " + str(fTestFile)
    #     print "fKeyFile: " + str(fKeyFile)
    #     argsIndex += 1

    fTestFile = sys.argv[1]
    fKeyFile = sys.argv[2]
    # print "fTestFile: " + str(fTestFile)
    # print "fKeyFile: " + str(fKeyFile)

    with open(fTestFile) as fT1:
        with open(fKeyFile) as fK1:
            contestTest = fT1.read()
            contentsKey = fK1.read()
            testTokens = generate_tokens(contestTest)
            keyTokens = generate_tokens(contentsKey)
        fT1.close()
        fK1.close()

    # for i in testTokens:
    #     for j in keyTokens:
    #         if i == j:
    #             print "Matched: " + str(i) + " " + str(j)
    #         else:
    #             print "Did not match: " + str(i) + " " + str(j)

    correctCount = 0
    incorrectCount = 0
    totalCount = 0

    for i in range(len(testTokens)):
        keyTokensValue = keyTokens[i]
        keyTokensValue = keyTokensValue.replace("\/", "")
        testTokensValue = testTokens[i]
        testTokensValue = testTokensValue.replace("\/", "")
        if testTokensValue == keyTokensValue:
            # print "It matched " + str(testTokensValue) + " " + str(keyTokensValue)
            testSplitTokens = testTokensValue.split('/')
            testPosToken = testSplitTokens[1]
            # print "testPosToken: " + testPosToken

            # if keyTokensValue[1] == '/':
            #     testingToken0 = keyTokensValue[0]
            #     testingToken2 = keyTokensValue[2]
            #
            #     print "testingToken0: " + testingToken0 + " testingToken2: " + testingToken2

            keySplitTokens = keyTokensValue.split('/')
            keyPosToken = keySplitTokens[1]

            # print "keyPosToken: " + keyPosToken

            correctCount += 1

            generate_confusion_matrix(keyTokenDict,testPosToken,keyPosToken)

        else:
            # print "Did not match " + str(testTokens[i]) + " " + str(keyTokensValue)
            testSplitTokens = testTokensValue.split('/')
            testPosToken = testSplitTokens[1]

            # print "testPosToken: " + testPosToken


            keySplitTokens = keyTokensValue.split('/')
            keyPosToken = keySplitTokens[1]

            # print "keyPosToken: " + keyPosToken

            incorrectCount += 1

            generate_confusion_matrix(keyTokenDict,testPosToken,keyPosToken)

    totalCount = correctCount + incorrectCount

    fractionCorrect = Fraction(correctCount,totalCount)
    fractionIncorrect = Fraction(incorrectCount,totalCount)

    # print "Correct: " + str(fractionCorrect)
    # print "Incorrect: " + str(fractionIncorrect)

    print str(float(fractionCorrect)*100) + "% CORRECT"
    print str(float(fractionIncorrect)*100) + "% INCORRECT"

    for keyToken in keyTokenDict:
        #for testToken in testTokenDict:
        for testToken in keyTokenDict.get(keyToken):
            print str(keyToken) + " " + str(testToken) + " " + str(keyTokenDict.get(keyToken).get(testToken))
        # print len(keyTokenDict.get(keyToken))
    # print len(keyTokenDict)

    # for key,val in keyTokenDict.items():
    #     print key, "=>", val

    # fileKey = open(fKeyFile)
#Dealing with the removing excess from key

def generate_confusion_matrix(keyTokenDict,testPosToken,keyPosToken):
    if keyPosToken in keyTokenDict:
                testTokenDict = keyTokenDict[keyPosToken]
                if testTokenDict is not None:
                    if testPosToken in testTokenDict:
                        testTokenDict[testPosToken] += 1
                    else:
                        testTokenDict[testPosToken] = 1
                else:
                    testTokenDict = { testPosToken : 1 }
                    keyTokenDict[keyPosToken] = testTokenDict
    else:
        testTokenDict = { testPosToken : 1 }
        keyTokenDict[keyPosToken] = testTokenDict


def generate_tokens(s):
    # print "loading in contents"
    # Convert to lowercases
    # s = s.lower()
    s = re.sub("[\[\]]", '', s)

    # Replace new lines with spaces
    s = re.sub(r'\s+', ' ', s)

    # Break sentence into the tokens, remove empty tokens
    tokens = [token for token in s.split(" ") if token != ""]

    stringToken = str(tokens)
    # print "tokens are: " + stringToken + "\n"

    return tokens

if __name__ == "__main__":
    main()
