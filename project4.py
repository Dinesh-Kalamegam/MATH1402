"""
Python Project 4
Nicholas Thompson (SN: 15019385)
Dinesh Kalamegam (SN: 16003714)

"""

""" Import Modules that we may need """
import numpy as np
import random as rand
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import math as math

""" Avoid the need to recompute the PI CONSTANTS """
pi = math.pi
halfPi = (math.pi)/2
threeHalfPi = 1.5 * (math.pi)
twoPi = 2*(math.pi)

"""Get the information from the files store as array """
# converts a line a0,b0,c0 to [a0,b0,c0]
inputfile = open('triangle_triples.data', 'r')
linesAsArrays = []
for line in inputfile:
    eachLine = []
    strlist = line.split()
    for i in range(len(strlist)):
        eachLine.append(strlist[i])

    linesAsArrays.append(eachLine)

# We shall use this dictionary to report the the highest and lowest probabilty
arrayProbability  = {}

# Find a probability given a triple
"""
In the file a < b < c so if we imagine the triangle to be plotted on a graph
    the side a is along the x axis
    the side b is along the y axis
"""

""" Given a triple we now want to find the probabilty of exiting each side"""
# Write it like this so we can just pass arrays from linesAsArrays
# Also this way we can change N easily too
def probability(arr,N):
    a , b , c  = int(arr[0]) ,int(arr[1]), int(arr[2])
    aCounter = bCounter = cCounter = 0

    for n in range(0,N):

        # Set up the triangle in the coordinate axis
        # Generate a random point in the triangle
        randomValue1 = rand.uniform(0,1)
        randomValue2 = rand.uniform(0,1)
        while(randomValue1 + randomValue2 > 1):
            randomValue1 = rand.uniform(0,1)
            randomValue2 = rand.uniform(0,1)
        x = a * randomValue1
        y = b * randomValue2

        # Generate a random angle for the ant to travel in
        theta = rand.uniform(0, twoPi)

        # Now model the ant travel in a straight line equation
        antGradient = math.tan(theta)
        bIntercept = y - (antGradient*x)
        aIntersect = bIntercept/-antGradient

        # The angle that the ant goes in can be considered as a quadrant
        quad1 = (0 <= theta and theta <= halfPi)
        quad2 = (halfPi <= theta and theta <= pi)
        quad3 = (pi <= theta and theta <= threeHalfPi)
        quad4 = (threeHalfPi <= theta and theta <= twoPi)

        # Checking which side the ant will cross
        if (quad1):
            cCounter +=1

        elif(quad2):
            if(bIntercept<b and bIntercept>0):
                bCounter+=1
            else:
                cCounter+=1

        elif(quad3) :
            if(aIntersect<a and aIntersect>0):
                aCounter+=1
            else:
                bCounter+=1

        elif(quad4):
            if(aIntersect>0 and aIntersect<a):
                aCounter+=1
            else:
                cCounter+=1

    printStatements(arr, aCounter, bCounter, cCounter, N)

    # We are filling the dictionary as {probability:triple}
    arrayProbability[cCounter/N]=arr

#Helper function that allows us to print tables.
def printStatements(array, a, b, c, n):

     print(
    array,"\n",
    "P(a) =" , a/n,"\n" ,
    "P(b) = ", b/n,"\n",
    "P(c) = ", c/n,"\n",
    "-------------------------------------------------------------")

#Returns the triangle that gives us the smallest probability and that probability.
def smallestProbability(sortedProbs):
    return arrayProbability[sortedProbs[0]], sortedProbs[0]

#Returns the triangle that gives us the largest probability and that probability.
def largestProbability(sortedProbs):
    return arrayProbability[sortedProbs[len(sortedProbs)-1]], sortedProbs[len(sortedProbs) -1]

# Plots the data for us.
def histogram(sortedProbs, n):
    # Finding the mean and Standard deviation of the probabilities
    mean = sum(list(arrayProbability.keys()))/(len(arrayProbability))
    sd = np.std(sortedProbs, axis=0)

    # plotting the histogram
    # in built plt.hist gives us less flexibility.
    # we will create intervals and calculate frequencies and then use plt.bar to plot our histogram.

    #get smallest probability
    a, b = smallestProbability(sortedProbs)
    #get largest probability
    c, d = largestProbability(sortedProbs)

    #number of intervals
    bins = 17
    #Gives us evenly spaced intervals between largest and smallest probability.
    intervals = np.linspace(b, d, bins)

    #initialise frequencies to zero.
    frequency = []
    for i in range(0,bins):
        frequency.append(0)

    #Calculate frequencies for each interval.
    for prob in sortedProbs:
        for j in range(1, len(intervals)):
            if(prob <= intervals[j]):
                frequency[j-1] = frequency[j-1] + 1
                break

    #x-axis values for neater display.
    roundInter = []
    for num in range(0,len(intervals)):
        if((num % 2) == 0):
            roundInter.append(round(intervals[num], 4))

    #Plot histogram to show how exit probabilities distributed across the triangles.
    f = plt.figure(1)
    width = 1.0
    axis = plt.axes()
    axis.set_xticklabels(roundInter)
    x_axis = np.arange(len(intervals))
    f.suptitle('Histogram that shows how the exit probabilities of side C are distributed across the triangles.' + '\n' + 'Histogram: N = {}, Mean = {}, Standard Deviation = {}'.format(n,round(mean,3), round(sd,3)))
    plt.xlabel('Exit Probability of side C.')
    plt.ylabel('Frequency of Triangles.')
    plt.bar(x_axis, frequency, width, color='r')
    #bbox_inches = 'tight' prevents the diagram being cropped 
    f.savefig("figure1",bbox_inches='tight')

    #Plot bar chart that shows how increasing length of the side c for triangles affects exit probability.
    g = plt.figure(2)
    array2 = list(arrayProbability.values())
    arrayb = []
    for i in range(0, len(array2)):
        arrayb.append(int(array2[i][2]))
    ax2 = plt.axes()
    ax2.set_xticklabels([])
    g.suptitle('Bar chart that shows how the lengths of side C of the triangles are distributed.' + '\n' + 'Histogram: N = {}, Mean = {}, Standard Deviation = {}'.format(n,round(mean,3), round(sd,3)))
    plt.xlabel('Triangles - One bar represents one triangle. Arranged in ascending order of length of side C.')
    plt.ylabel('Exit Probability for side C')
    plt.bar(range(len(arrayb)), list(arrayProbability.keys()),width, color='r')
    g.savefig("figure2",bbox_inches='tight')


"""
This function is responsible for printing out data and execution of the whole
program.
"""
def start():

    #WE NEED THIS LINE FOR THE VALIDATION
    print("################################################################")

    print("First we validate the 3,4,5 triple using the method \n")
    print(probability([3,4,5],10000000))

    print("################################################################ \n")

    Npass = 10000
    print("Exit probabilties for triangles in file that N = " +str(Npass) +"\n")

    for array in linesAsArrays:
        probability(array,Npass)

    print("################################################################ \n")
    """ Section for finding largest and smallest probabilities """

    # We can sort by keys, the keys of the dictionary are the probabilities
    sortedProbabilities = sorted(arrayProbability)

    print("The smallest probability of exiting the longest side is given by: ")
    # The lowest key value in the dictionary gives us the triangle i.e. a.
    a, b = smallestProbability(sortedProbabilities)
    print(a)
    print("With exit probability on side c as: ")
    # The first value in sortedProbabilities gives us the probability i.e. b.
    print(b)
    print('\n')
    print("The largest probability of exiting the longest side is given by ")
    # The largest key value in the dictionary gives us the triangle i.e. c.
    c, d = largestProbability(sortedProbabilities)
    print(c)
    print("With exit probability on side c as: ")
    # The last value in sortedProbabilities gives us the probability i.e. d.
    print(d)
    print("\n")

    print("################################################################ \n")
    """ Making the histogram """

    histogram(sortedProbabilities, Npass)

    print("Histogram saved to file.")

#Call the start function.
start()
