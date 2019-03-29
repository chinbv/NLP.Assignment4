# -*- coding: utf-8 -*-
##############################################################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################
#####
##### Brandon Chin
##### Monday, March 29th, 2019
##### CMSC 416 - Natural Language Processing
##### Programming Assignment 4 - Decision-list
#####
##### 1. The Problem
##### Write a Perl (or Python3) program called decision-list.pl that implements a decision list classifier to perform word sense disambiguation.
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

myBagOfWords={}
# text_file = None


def main():##main method


    # print("This program tags words with POS.")
    # print("Created by Brandon Chin")

    trainingFilename = sys.argv[1]

    myBagOfWords = generate_bagOfWords(trainingFilename)

    # create featureVector for first feature
    feature1Vector = myBagOfWords.copy()

    feature1Training(feature1Vector, trainingFilename)

    # print("feature1Vector is " + str(feature1Vector))

    # create featureVector for second feature
    feature2Vector = myBagOfWords.copy()

    feature2Training(feature2Vector, trainingFilename)

    # print("feature2Vector is " + str(feature2Vector))

    # create featureVector for third feature
    feature3Vector = myBagOfWords.copy()

    feature3Training(feature3Vector, trainingFilename)

    # print("feature3Vector is " + str(feature3Vector))


    # create featureVector for fourth feature
    feature4Vector = myBagOfWords.copy()

    feature4Training(feature4Vector, trainingFilename)

    # print("feature4Vector is " + str(feature4Vector))

    decisionListFunctions=[]
    decisionListVectors=[]

    decisionListFunctions.append(evaluateFeature1)
    decisionListFunctions.append(evaluateFeature2)
    decisionListFunctions.append(evaluateFeature3)
    decisionListFunctions.append(evaluateFeature4)
    decisionListVectors.append(feature1Vector)
    decisionListVectors.append(feature2Vector)
    decisionListVectors.append(feature3Vector)
    decisionListVectors.append(feature4Vector)

    testFilename = sys.argv[2]

    evaluateTestFile(testFilename, decisionListFunctions, decisionListVectors, sys.argv[3])



def contextLinesFromTrainingFile(filename):

    loadFileName = filename
    f = open(loadFileName,"r")
    contents = f.readlines()
    f.close()

    phoneContextLines=[]
    phoneToken = None
    aboutToCollectContents = False

    for line in contents:
        if "<answer" in line:
            answerLine = line
            # print ("answerLine: " + answerLine)

                # print("line is: " + line)

                #phonePattern = re.compile(r'phone')
            phoneMatch = re.search('phone', answerLine)
                # print "cardinalMatch " + str(cardinalMatch)

            if phoneMatch is not None:
                phoneToken = phoneMatch.group()

            # print ("senseid is a " + str(phoneToken))

        if "<context>" in line and phoneToken == 'phone':
            aboutToCollectContents = True
        else:
            if aboutToCollectContents == True:
                # Replace new lines with spaces
                line = re.sub(r'\s+', ' ', line)

                line = line.lower()

                # print("Line before the stopWords: " + line)

                # List of stopWords to be removed
                stopWords=['a','an','and','are','as','at','be','by','for','from','has','he','in',
                'is','it','its','of','on','that','the','to','was','were','will','with']

                tagWords=['<s>','</s>','<@>','<p>','</p>']

                punctuation=[',','.','!','?','"','--']

                line = ' '.join([word for word in line.split() if word not in stopWords])

                line = ' '.join([word for word in line.split() if word not in tagWords])

                line = ' '.join([word for word in line.split() if word not in punctuation])

                # print("Line after the stopWords: " + line)

                phoneContextLines.append(line)
                aboutToCollectContents = False
                phoneToken = None

    return phoneContextLines

#generating the bag of words
def generate_bagOfWords(trainingFilename):

    contextLines = contextLinesFromTrainingFile(trainingFilename)

    for line in contextLines:
        # Break sentence into the tokens, remove empty tokens
        tokens = [token for token in line.split(" ") if token != ""]

        # Adding tokens to myBagOfWords for untrained featureVector
        for currToken in tokens:
            if currToken not in myBagOfWords:
                myBagOfWords[currToken] = 0

    # print(myBagOfWords)
    # print ("size of myBagOfWords = " + str(len(myBagOfWords.keys())))

    return myBagOfWords

def evaluateTestFile(filename, decisionListFunctions, decisionListVectors, logFilename):

    loadFileName = filename
    f = open(loadFileName,"r")
    contents = f.readlines()
    f.close()

    log_file = open(logFilename,"w")
    # print ("log_file is " + str(log_file))
    #
    # if log_file == None:
    #     print ("log_file is none")

    aboutToCollectContents = False
    instanceLine = None

    for line in contents:
        if "<instance" in line:
            instanceLine = line
            instanceLine = re.sub(r'<instance id=', '', instanceLine)
            instanceLine = re.sub(r'>', ' ', instanceLine)
            instanceLine = re.sub(r'\s+', ' ', instanceLine)

            # print ("instanceLine: " + instanceLine)

        if "<context>" in line:
            aboutToCollectContents = True
        else:
            if aboutToCollectContents == True:
                # Replace new lines with spaces
                line = re.sub(r'\s+', ' ', line)

                line = line.lower()

                # print("Line before the stopWords: " + line)

                # List of stopWords to be removed
                stopWords=['a','an','and','are','as','at','be','by','for','from','has','he','in',
                'is','it','its','of','on','that','the','to','was','were','will','with']

                tagWords=['<s>','</s>','<@>','<p>','</p>']

                punctuation=[',','.','!','?','"','--']

                line = ' '.join([word for word in line.split() if word not in stopWords])

                line = ' '.join([word for word in line.split() if word not in tagWords])

                line = ' '.join([word for word in line.split() if word not in punctuation])

                # print("Line after the stopWords: " + line)

                evaluateFeatures(instanceLine, line, decisionListFunctions, decisionListVectors,log_file)
                aboutToCollectContents = False
    log_file.close()

def evaluateFeatures(instanceLine, contextLine, decisionListFunctions, decisionListVectors,log_file):
    # print("<answer instance=" + instanceLine)

    resultBoolean = False
    featureIndex = 0

    # if log_file == None:
    #     print ("logFile is none")

    while(resultBoolean == False and featureIndex < len(decisionListFunctions)):
        resultBoolean = decisionListFunctions[featureIndex](decisionListVectors[featureIndex],instanceLine,contextLine)

        if resultBoolean == True:
            senseid = "phone"
            log_file.write("feature["+str(featureIndex)+"] selected senseid=\"" + str(senseid)+"\""+"\n")
        else:
            log_file.write("feature["+str(featureIndex)+"] did not select senseid=\"phone\""+"\n")
        featureIndex += 1
    if(resultBoolean == False):
        # none of the evaluations resulted in phone, so then assuming it is a product
        senseid = "product"
        log_file.write("Selected senseid=\"" + str(senseid)+"\""+"\n")

    print("<answer instance=" + instanceLine + "senseid=\""+senseid+"\"/>")



def evaluateFeature1(feature1Vector,instanceLine,contextLine):
    returnValue = False

    contextLineList = contextLine.split("<head>")
    if len(contextLineList) == 2:##the target word is at the start of the line, so no before string
        beforeString = contextLineList[0]
        beforeStringTokens = beforeString.split(" ")
        lastToken = beforeStringTokens[-2] #because -1 is an ending space

        value = feature1Vector.get(lastToken)
        if value is not None and value == 1:
            returnValue = True
        # print("beforeString is " + str(beforeString))
        # print("beforeStringTokens is " + str(beforeStringTokens))
        # print("lastToken is " + lastToken)

    return returnValue

def evaluateFeature2(feature2Vector,instanceLine,contextLine):
    returnValue = False

    contextLineList = contextLine.split("<head>")
    if len(contextLineList) == 2:##the target word is at the start of the line, so no before string
        beforeString = contextLineList[0]
        beforeStringTokens = beforeString.split(" ")
        if len(beforeStringTokens) >= 3:
            lastToken = beforeStringTokens[-3] #because -1 is an ending space

            value = feature2Vector.get(lastToken)
            if value is not None and value == 1:
                returnValue = True
        # print("beforeString is " + str(beforeString))
        # print("beforeStringTokens is " + str(beforeStringTokens))
        # print("lastToken is " + lastToken)

    return returnValue

def evaluateFeature3(feature3Vector,instanceLine,contextLine):
    returnValue = False

    contextLineList = contextLine.split("<head>")
    if len(contextLineList) == 2:##the target word is at the start of the line, so no before string
        afterString = contextLineList[1]
        afterStringTokens = afterString.split(" ")
        if len(afterStringTokens) >= 2:
            firstToken = afterStringTokens[1]

            value = feature3Vector.get(firstToken)
            if value is not None and value == 1:
                returnValue = True
            # print("beforeString is " + str(beforeString))
            # print("beforeStringTokens is " + str(beforeStringTokens))
            # print("[Test] firstToken is " + firstToken)

    return returnValue

def evaluateFeature4(feature4Vector,instanceLine,contextLine):
    returnValue = False

    contextLineList = contextLine.split("<head>")
    if len(contextLineList) == 2:##the target word is at the end of the line, so no after string
        afterString = contextLineList[1]
        afterStringTokens = afterString.split(" ")
        if len(afterStringTokens) >= 3:
            firstToken = afterStringTokens[2]

            value = feature4Vector.get(firstToken)
            if value is not None and value == 1:
                returnValue = True
        # print("beforeString is " + str(beforeString))
        # print("beforeStringTokens is " + str(beforeStringTokens))
        # print("[Test] firstToken is " + firstToken)

    return returnValue


#Feature gets the word before the <head> tag
def feature1Training(feature1Vector, trainingFilename):

    contextLines = contextLinesFromTrainingFile(trainingFilename)

    for contextLine in contextLines:
        contextLineList = contextLine.split("<head>")
        if len(contextLineList) == 2:##the target word is at the start of the line, so no before string

            beforeString = contextLineList[0]
            beforeStringTokens = beforeString.split(" ")
            if len(beforeStringTokens) >= 2:
                lastToken = beforeStringTokens[-2] #because -1 is an ending space

                # print("beforeString is " + str(beforeString))
                # print("beforeStringTokens is " + str(beforeStringTokens))
                # print("lastToken is " + lastToken)

                feature1Vector[lastToken] = 1
                # print(lastToken +" was added to vector")

    return feature1Vector

#Feature gets the word 2 before the <head> tag
def feature2Training(feature2Vector, trainingFilename):

    contextLines = contextLinesFromTrainingFile(trainingFilename)

    for contextLine in contextLines:
        contextLineList = contextLine.split("<head>")
        if len(contextLineList) == 2:##the target word is at the start of the line, so no before string
            beforeString = contextLineList[0]
            beforeStringTokens = beforeString.split(" ")
            if len(beforeStringTokens) >= 3:
                lastToken = beforeStringTokens[-3]

                feature2Vector[lastToken] = 1

                # print(lastToken +" was added to vector")

    return feature2Vector

#Feature gets the word after the <head> tag
def feature3Training(feature3Vector, trainingFilename):

    contextLines = contextLinesFromTrainingFile(trainingFilename)

    for contextLine in contextLines:
        contextLineList = contextLine.split("<head>")
        if len(contextLineList) == 2:##the target word is at the end of the line, so no after string

            afterString = contextLineList[1]
            afterStringTokens = afterString.split(" ")
            if len(afterStringTokens) >= 2:
                firstToken = afterStringTokens[1]


                feature3Vector[firstToken] = 1

                # print("contextLineList is " + str(contextLineList))
                # print("afterString is " + str(afterString))
                # print("afterStringTokens is " + str(afterStringTokens))
                # print("[Training] firstToken is " + firstToken)

            # print(firstToken +" was added to vector")

    return feature3Vector

#Feature gets the word 2 after the <head> tag
def feature4Training(feature4Vector, trainingFilename):

    contextLines = contextLinesFromTrainingFile(trainingFilename)

    for contextLine in contextLines:
        contextLineList = contextLine.split("<head>")
        if len(contextLineList) == 2:##the target word is at the end of the line, so no after string
            afterString = contextLineList[1]
            afterStringTokens = afterString.split(" ")
            if len(afterStringTokens) >= 3:
                firstToken = afterStringTokens[2]

                feature4Vector[firstToken] = 1

                # print(firstToken +" was added to vector")

            # print("contextLineList is " + str(contextLineList))
            # print("afterString is " + str(afterString))
            # print("afterStringTokens is " + str(afterStringTokens))
            # print("[Training] firstToken is " + firstToken)

    return feature4Vector


if __name__ == "__main__":
    main()
