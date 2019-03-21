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


import re
import sys
from decimal import Decimal
from random import *
import operator

wordDict = {}

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

    while argsIndex <= numberOfArgs:
        loadFileName = sys.argv[argsIndex]
        # print "opening file " + loadFileName
        f = open(loadFileName,"r")
        contents = f.read()
        f.close()
        # print contents + "\n"
        if argsIndex == 1:
            # print "I got here [1]"
            generate_tokens(contents)
        if argsIndex == 2:
            # print "I got here [2]"
            generate_testTokens(contents)
        # print "argsIndex: " + argsIndex
        argsIndex += 1

    # loadFileName = trainingData
    # print "opening file " + loadFileName
    # f = open(loadFileName,"r")
    # contents = f.read()
    # f.close()
    # # print contents + "\n"
    # generate_tokens(contents)

    # loadFileName = testData
    # print "opening file " + loadFileName
    # f = open(loadFileName,"r")
    # contents = f.read()
    # f.close()
    # print contents + "\n"
    # generate_testTokens(contents)

    # print (generate_sentences(ngramDict))



    # counts = dict()

#Dealing with the test file tokens
def generate_testTokens(s):

    # Replace new lines with spaces
    s = re.sub(r'\s+', ' ', s)

    # Break sentence into the tokens, remove empty tokens
    tokens = [token for token in s.split(" ") if token != ""]

    for i in range(len(tokens)):
        #print "Tokens {}: {}".format(i+1, tokens[i])
        currToken = tokens[i]

        punct = ['!',',','.','?']

        # print "CurrToken: " + currToken + "\n"

        # wordDictCheck = wordDict.get(currToken, None)

        # print "wordDictCheck: " + str(wordDictCheck)

        # if wordDictCheck == "None":
        #     print "Did not exist in wordDict"
        #     generate_frequencies(currToken, "NN", wordDict)
        #     print "should have inserted it"


        capitalPattern = re.compile(r'[A-Z]\S+')
        capitalMatch = capitalPattern.match(''.join(currToken))
        capitalToken = None
        if capitalMatch != None:
            capitalToken = capitalMatch.group()
            # print "capitalToken is " + str(capitalToken)

        cardinalPattern = re.compile(r'[0-9].+')
        cardinalMatch = cardinalPattern.match(''.join(currToken))
        # print "cardinalMatch " + str(cardinalMatch)
        cardinalToken = None
        if cardinalMatch != None:
            cardinalToken = cardinalMatch.group()

            # print "cardinalGroup " + str(cardinalGroup)

        specificEndingPattern = re.compile(r'\w+(?:\?|\.|ly\b)')
        endingMatch = specificEndingPattern.match(''.join(currToken))
        endingToken = None
        if endingMatch != None:
            endingToken = endingMatch.group()
            # print "capitalToken is " + str(capitalToken)

        specificStartPattern = re.compile(r'\b[unUn]\w+')
        startMatch = specificStartPattern.match(''.join(currToken))
        unToken = None
        if startMatch != None:
            unToken = startMatch.group()
            # print "capitalToken is " + str(capitalToken)

        specificStart1Pattern = re.compile(r'\b[inIn]\w+')
        start1Match = specificStart1Pattern.match(''.join(currToken))
        inToken = None
        if start1Match != None:
            inToken = start1Match.group()
            # print "capitalToken is " + str(capitalToken)



        # capitalSearchTerm = re.search(capitalPattern, currToken)
        # capitalToken = capitalSearchTerm.group()
        #
        # print "CAPITAL TOKEN: " + str(capitalToken)
        # cardinalToken = re.search(cardinalPattern, currToken)
        # endingToken = re.search(specificEndingPattern, currToken)
        # unToken = re.search(specificStartPattern, currToken)
        # inToken = re.search(specificStart1Pattern, currToken)
        # if capitalToken.group() != None:
        #     capitalToken.group()
        #     print "capitalToken match: " + str(capitalToken)


        def openBracket():
            print "[",

        def closeBracket():
            print "]"

        def capitalNoun():
            # print "REACHED HERE"
            theMaxPOS = "NNP"
            print currToken + "/" + str(theMaxPOS)
        def cardinalNumber():
            # print "REACHED HERE"
            theMaxPOS = "CD"
            print currToken + "/" + str(theMaxPOS)
        def specificEnding():
            theMaxPOS = "RB"
            print currToken + "/" + str(theMaxPOS)

        def specificStart():
            theMaxPOS = "JJ"
            print currToken + "/" + str(theMaxPOS)

        def specificStart1():
            theMaxPOS = "JJ"
            print currToken + "/" + str(theMaxPOS)

        def default():
            #print "default:"

            resultingPOS = wordDict.get(currToken,None)
            # print "resultingPOS: " + str(resultingPOS)
            theMaxPOS = findMostFrequent(resultingPOS)
            # cardinalNumber = re.compile(r'[0-9]')
            # if cardinalNumber.match(''.join(currToken)):
            #     theMaxPOS = "CD"
            # print "theMaxPOS: " + str(theMaxPOS)
            # for i in punct:
            #     # print i
            #     if theMaxPOS == i:
            #         print currToken + "/" + theMaxPOS
            #     else:
            #         print currToken + "/" + theMaxPOS,
            print currToken + "/" + str(theMaxPOS)

        switcher = {
            '[': openBracket,
            ']': closeBracket,
            capitalToken: capitalNoun,
            cardinalToken: cardinalNumber,
            endingToken: specificEnding,
            unToken: specificStart,
            inToken: specificStart1,
        }

        def switch(currToken):
            #print "I got here [1] " + currToken
            return switcher.get(currToken, default)()

        switch(currToken)

        # if currToken == "]" or currToken == "[":
        #     print "Token was a ]: " + currToken
        #     print "]"
        # if currToken == "[":
        #     print "Token was a [: " + currToken
        #     print "["
        # else:
        #     print "in else statement, currToken " + currToken

            # print "Word: " + currToken + " POS: " + theMaxPOS


    # stringToken = str(tokens)
    # create_tokens(tokens, wordDict)

    # print "stringToken are " + stringToken + "\n"
    # print "firstWord is " + str(firstWord) + "\n"


    # print "Tokens are " + str(tokens) + "\n"

#Find most frequent occurence in posDict
def findMostFrequent(resultingPOS):

    maxPOS = None
    maxFreq = 0

    # print "resultingPOS: " + str(resultingPOS)

    if resultingPOS == None:
        # print "Did not exist in wordDict"
        maxPOS = "NN"
        # print "should have inserted it"


    else:
        for pos,frequency in resultingPOS.items():
            if maxFreq < frequency:
                maxFreq = frequency
                maxPOS = pos
        # print "(inside for loop) maxPOS: " + maxPOS
    # print "(outside for loop) maxPOS: " + maxPOS


    # def emptyPos():
    #     maxPOS = "NN"
    #
    # def closeBracket():
    #     print "]"
    #
    # def default():
    #     #print "default:"
    #     resultingPOS = wordDict.get(currToken,None)
    #     # print "resultingPOS: " + str(resultingPOS)
    #     theMaxPOS = findMostFrequent(resultingPOS)
    #     # print "theMaxPOS: " + str(theMaxPOS)
    #     # for i in punct:
    #     #     # print i
    #     #     if theMaxPOS == i:
    #     #         print currToken + "/" + theMaxPOS
    #     #     else:
    #     #         print currToken + "/" + theMaxPOS,
    #     print currToken + "/" + str(theMaxPOS)
    #
    # switcher = {
    #     '[': openBracket,
    #     ']': closeBracket,
    # }
    #
    # def switch(currToken):
    #     #print "I got here [1] " + currToken
    #     return switcher.get(currToken, default)()
    #
    # switch(currToken)

    return maxPOS

#Dealing with the training file tokens
def generate_tokens(s):
    # print "loading in contents"
    # Convert to lowercases
    # s = s.lower()

    # Replace all brackets with empty
    s = re.sub("[\[\]]", '', s)

    # Replace new lines with spaces
    s = re.sub(r'\s+', ' ', s)

    # Break sentence into the tokens, remove empty tokens
    tokens = [token for token in s.split(" ") if token != ""]

    # stringToken = str(tokens)
    create_tokens(tokens, wordDict)

    # for key,val in wordDict.items():
    #     print key, "=>", val

    # print "stringToken are " + stringToken + "\n"
    # print "firstWord is " + str(firstWord) + "\n"

    # print "Tokens are " + str(tokens) + "\n"



#split the 3 part token into 3 individual parts
def create_tokens(tokens, wordDict):

    # wordToken = [stringToken for stringToken in stringToken.split('/') if stringToken !=""]
    # posToken = [stringToken for stringToken in stringToken.split('/') if stringToken !=""]
    # print tokens

    for i in range(len(tokens)):
        # print "Tokens {}: {}".format(i+1, tokens[i])
        currToken = tokens[i]
        # print "currToken: " + currToken
        splitTokens = currToken.split('/')
        # if currToken == '[':
        #     print "token is " + currToken
        # if currToken == ']':
        #     print "token is " + currToken
        # else:
        # print "splitTokens are " + str(splitTokens) + "\n"

        wordToken = splitTokens[0]

        posToken = splitTokens[1]

        # capitalLetter = re.compile(r'.*?[A-Z].*?')
        # if capitalLetter.match(''.join(wordToken)):
        #     posToken = "NNP"

        generate_frequencies(wordToken, posToken, wordDict)

        # for word in wordDict:
        #     print "wordDict contains " + word + "\n"

        # print "wordToken is " + str(wordToken) + "\n"
        # print "posToken is " + str(posToken) + "\n"

    # tokenDict.append(wordToken)

    # print "PosToken are " + posToken + "\n"

def generate_frequencies(wordToken, posToken, wordDict):

    if wordToken in wordDict:
                # print "incrementing posDict " + wordToken + " count"
                posDict = wordDict[wordToken]
                if posDict is not None:
                    if posToken in posDict:
                        posDict[posToken] += 1
                    else:
                        posDict[posToken] = 1
                else:
                    posDict = { posToken : 1 }
                    wordDict[wordToken] = posDict
    else:
        # print "adding wordToken " + "|" + wordToken + "|" + " to wordDict"
        posDict = { posToken : 1 }
        wordDict[wordToken] = posDict
        # print ("Buffer after newNgram is added to ngramDict " + " len(lookBackBuffer): " + str(len(lookBackBuffer))
        #     + " ngramSize: " + str(ngramSize))
    # for key,val in wordDict.items():
    #     print key, "=>", val
    # for key,val in posDict.items():
    #     print key, "=>", val
    # findMostFrequent(posDict)


if __name__ == "__main__":
    main()
