from collections import Counter
import itertools
#do in py27

# Simple HMM with exhaustive search
#
#DefineHMM
#
#States         #nucleic acid tag
stateToIdxLUT = {'tag1':0, 'tag2':1, 'tag3':2}
idxToStateLUT = ['tag1', 'tag2', 'tag3']
allTags = idxToStateLUT     

#Observations   #3 amino acids
emissToIdxLUT = {'ata':0, 'tgc':1, 'ggg':2,}
idxToEmissLUT = ['ata', 'tgc', 'ggg']
allWords = idxToEmissLUT    

# Transition matrix (from/to states)
transMatrix = [[0.2, 0.6, 0.2],
               [0.3, 0.3, 0.4],
               [0.1, 0.8, 0.1]]

# Emissions matrix (state/emission)
emissMatrix = [[0.25, 0.50, 0.25,],
               [0.05, 0.95, 0.0],
               [0.4, 0.2, 0.4]]

# Start probabilities (state)
startProbs = [1.0, 0.0, 0.0]




#
# HMM Functions
#
# seq: List of elements in sequence(e.g. ['tgc', 'ggg', 'ata'])
def findTagSequence(sent):
    # Step 1: Generate all possible tag sequences
    length = len(sent)
    possibleTagSeq = list( itertools.product(idxToStateLUT, repeat=length) )

    bestTags = []
    bestProb = -1.0
    for tagSeq in possibleTagSeq:
        probSeq = calcProb(sent, tagSeq)

        # Check to see if this beats the current-best (i.e. most probable) tag sequence
        if (probSeq > bestProb):
            bestProb = probSeq
            bestTags = tagSeq 

    # Return the most probable tag sequence, and it's probability
    return (bestTags, bestProb)


# Supporting function for findTagSequence
# Calculates the probability for a given tag sequence given some sentence
def calcProb(sent, tagSeq):
    # Recall Order: Transition, emission, transition, emission, ...
    runningProd = 1

    # Initial state: use start probabilities
    for curIdx in range(0, len(sent)):
        curTag = tagSeq[curIdx]
        curWord = sent[curIdx]

        probTrans = 0
        probEmiss = 0

        if (curIdx == 0):
            # Start State
            probTrans = startProbs[ stateToIdxLUT[curTag] ]
            probEmiss = emissMatrix[stateToIdxLUT[curTag]][emissToIdxLUT[curWord]]
        else :
            # Non-start state
            lastTag = tagSeq[curIdx-1]
            probTrans = transMatrix[stateToIdxLUT[lastTag]][stateToIdxLUT[curTag]]
            probEmiss = emissMatrix[stateToIdxLUT[curTag]][emissToIdxLUT[curWord]] 

        runningProd *= probTrans * probEmiss

    # return probability
    return runningProd

#
# Supporting functions
#

# Words: list of words in the vocabulary
# maxLength: maximum length of sentence
def makeAllPossibleSentences(words, maxLength):
    out = []

    for length in range(1, maxLength+1):
        for onePerm in itertools.product(words, repeat = length):
            out.append( onePerm )

    return out


#
# Helper functions
#
def make2DList(n, m, defaultValue):
    list = [[defaultValue]*m for x in xrange(n)]
    return list


def printTable(maxDoors, maxOpenedDoors, data): #Copied from Monte Carlo assignment
    # table header
    print ("       ",)
    for numDoors in range(0, maxDoors-1):
        print ("{0: <6}".format(numDoors+1)),       # data
    print ("")      # new line

    # data
    for numOpenedDoors in range(0, maxOpenedDoors-1):
        print (str(numOpenedDoors+1) + "    "),          
        for numDoors in range(0, maxDoors-1):
            print ("{0: <6.1f}".format(data[numDoors][numOpenedDoors])),       # data
        print ("")      # new line


#
# Function to loop over data
#
def doRun(sentences):
    # Table Header
    print("{:30s}".format("Sequence") + "{:30s}".format("Tag Sequence") + "{:7s}".format("Product"))
    # Data
    for sent in sentences:
        (tagSeq, prob) = findTagSequence(sent)
        sentStr = "{:30s}".format(sent)
        tagSeqStr = "{:30s}".format(tagSeq)
        prodStr = "{0:.4f}".format(prob)

        print (sentStr + tagSeqStr + prodStr)



# Main program

# Step 1: Make all possible 3-word sequences
maxSentLength = 3
allSentences = makeAllPossibleSentences(allWords, maxSentLength)

# Step 2: Find tag sequences for each sentence
doRun(allSentences)

