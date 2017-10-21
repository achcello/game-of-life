import numpy as np
import matplotlib.pyplot as plt
import imageio

#populate the field as a list of lists with type int zeroes
(n,m) = (20,20)   #Define the size of the field
field = np.zeros( (n,m), dtype=np.int )

#number of generations to run
generations = 65

#assign initial condition
'''R-pentamino
field[10,10] = 1
field[9,10] = 1
field[11,10] = 1
field[9,11] = 1
field[10,9] = 1
'''

'''glider'''
field[0,1] = 1
field[1,2] = 1
field[2,0] = 1
field[2,1] = 1
field[2,2] = 1


plt.title('Initial Condition (generation = 0)')
plt.imshow( field )
plt.show()
plt.clf()

def GOL( field ):
    def get(l, p):
        try:
            return l[p]
        except IndexError:
            return 0

    def getL(l, p):
        try:
            return l[p]
        except IndexError:
            return [0]

    #define logic used to decide whether cell lives, dies, or is born
    def output( inputMatrix ):
        neighbors = inputMatrix[ 1: ]
        if inputMatrix[0] == 0:
            if neighbors.count(1) == 3:
                nextState = 1
                return nextState
            else:
                nextState = 0
                return nextState
        elif inputMatrix[0] == 1:
            if neighbors.count(1) < 2:
                nextState = 0
                return nextState
            elif (neighbors.count(1) == 2 or neighbors.count(1) == 3):
                nextState = 1
                return nextState
            elif neighbors.count(1) > 3:
                nextState = 0
                return nextState

    newfield = field.copy()

    currentCases = {}

    #getCase() retrieves the states of the neighboring cells and puts them into a list to be read by output()
    def getCase( i,j ):
        currentCase = []
        def addN( addition ):
            currentCase.append( addition )
        addN( get(getL(field,i),j) )
        addN( get(getL(field,i-1),j-1) )
        addN( get(getL(field,i-1),j) )
        addN( get(getL(field,i-1),j+1) )
        addN( get(getL(field,i),j-1) )
        addN( get(getL(field,i),j+1) )
        addN( get(getL(field,i+1),j-1) )
        addN( get(getL(field,i+1),j+1) )
        addN( get(getL(field,i+1),j) )
        return currentCase

    for i in range( field.shape[0] ):
        for j in range( field.shape[1] ):
            currentCases[ (i,j) ] = getCase( i,j )
    for (coordinate,case) in currentCases.items():
        newfield[ coordinate[0],coordinate[1] ] = output( case )

    return newfield

newf = field.copy()
filenames = []

for gen in range(1,generations+1):
    newf = GOL( newf )
    plt.title('(generation = %s)' % gen)
    plt.imshow( newf )
    #plt.show()
    plt.savefig('generation_%s.png' % gen)
    filenames.append('generation_%s.png' % gen)
    plt.clf()
    
images = []
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('gol.gif', images, duration = 0.01)