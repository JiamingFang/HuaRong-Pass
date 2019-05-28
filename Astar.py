from queue import PriorityQueue as PriorityQ

class state:
    def __init__(self,T,parent,cost):
        self.T = T
        self.parent = parent
        self.cost = cost+1

        
def read_puzzle(id):
    puzzle = state([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],-1)

    f=None
    if id == 1:
        f = open("puzzle1.txt", "r")
        print("1")
    else:
        f = open("puzzle2.txt", "r")
        print("2")
    
    i=0
    while(i<5):
        line = f.readline()
        j = 0
        for c in line:
            if c!="\n":
                #print("line")
                puzzle.T[i][j] = c
                j+=1
        i+=1
        #print("A")
    f.close()

    print(puzzle.T)
    print(puzzle.parent)
    print(puzzle.cost)


def is__goal(state):
    if state.T[4][1] == 1 and  state.T[4][2] == 1 and state.T[3][1] == 1 and state.T[3][2] == 1:
        return True
    else:
        return False


def get_successors(state):
    zero1 = None
    zero2 = None
    successors = []
    for i in range(5):
        for j in range(4):
            if state.T[i][j] == 0:
                if(zero1 == None):
                    zero1 = [i,j]
                else:
                    zero2 = [i,j]
    #check if there are single pieces around both spaces that can be moved into the space
    #first move a piece down
    if zero1[0] != 0 and state.T[zero1[0]-1,zero1[1]] == 7:
        puzzle = state(state.T,state.T,state.cost)
        puzzle.T[zero1[0],zero1[1]] = 7
        puzzle.T[zero1[0]-1,zero1[1]] = 0
        successors.extend(puzzle)

    if zero2[0] != 0 and state.T[zero2[0]-1,zero2[1]] == 7:
        puzzle = state(state.T,state.T,state.cost)
        puzzle.T[zero2[0],zero2[1]] = 7
        puzzle.T[zero2[0]-1,zero2[1]] = 0
        successors.extend(puzzle)

    #move a piece up
    if zero1[0] != 4 and state.T[zero1[0]+1,zero1[1]] == 7:
        puzzle = state(state.T,state.T,state.cost)
        puzzle.T[zero1[0],zero1[1]] = 7
        puzzle.T[zero1[0]+1,zero1[1]] = 0
        successors.extend(puzzle)

    if zero2[0] != 4 and state.T[zero2[0]+1,zero2[1]] == 7:
        puzzle = state(state.T,state.T,state.cost)
        puzzle.T[zero2[0],zero2[1]] = 7
        puzzle.T[zero2[0]+1,zero2[1]] = 0
        successors.extend(puzzle)

    #move a piece left
    if zero1[1] != 3 and state.T[zero1[0],zero1[1]+1] == 7:
        puzzle = state(state.T,state.T,state.cost)
        puzzle.T[zero1[0],zero1[1]] = 7
        puzzle.T[zero1[0],zero1[1]+1] = 0
        successors.extend(puzzle)

    if zero2[1] != 3 and state.T[zero2[0],zero2[1]+1] == 7:
        puzzle = state(state.T,state.T,state.cost)
        puzzle.T[zero2[0],zero2[1]] = 7
        puzzle.T[zero2[0],zero2[1]+1] = 0
        successors.extend(puzzle)

    #move a piece right
    if zero1[1] != 0 and state.T[zero1[0],zero1[1]-1] == 7:
        puzzle = state(state.T,state.T,state.cost)
        puzzle.T[zero1[0],zero1[1]] = 7
        puzzle.T[zero1[0],zero1[1]-1] = 0
        successors.extend(puzzle)

    if zero2[1] != 0 and state.T[zero2[0],zero2[1]-1] == 7:
        puzzle = state(state.T,state.T,state.cost)
        puzzle.T[zero2[0],zero2[1]] = 7
        puzzle.T[zero2[0],zero2[1]-1] = 0
        successors.extend(puzzle)

    #now all the single pieces are done, move the 1*2 pieces



read_puzzle(1)

