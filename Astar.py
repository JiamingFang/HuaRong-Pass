from queue import PriorityQueue as PQ
import queue
import copy
import sys

class State:
    def __init__(self,T,parent,cost):
        self.T = copy.deepcopy(T)
        self.parent = parent
        self.cost = cost+1
    
    def __lt__(self, other):
        return self.cost < other.cost

    def toString(self):
        s = ""
        for i in range(5):
            for j in range(4):
                s+=str(self.T[i][j])
        return s

    def toOutput(self):
        s = ""
        for i in range(5):
            j = 0
            while j < 4:
                if self.T[i][j] == 0:
                    s+="0"
                elif self.T[i][j] == 1:
                    s+="1"
                elif self.T[i][j] == 7:
                    s+="4"
                elif j < 3 and self.T[i][j] == self.T[i][j+1]:
                    s+="22"
                    j+=1
                else:
                    s+="3"
                j+=1
            s+="\n"
        return s

     
def read_puzzle(id):
    init = State([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],-1)

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
                init.T[i][j] = int(c)
                j+=1
        i+=1
        #print("A")
    f.close()
    return init

    # print(puzzle.T)
    # print(puzzle.parent)
    # print(puzzle.cost)


def is_goal(state):
    return state.T[4][1] == 1 and  state.T[4][2] == 1 and state.T[3][1] == 1 and state.T[3][2] == 1


def get_cost(state):
    return state.cost


def get_heuristic(state):
    topLeft = None
    for i in range(5):
        flag = False
        for j in range(4):
            if state.T[i][j] == 1:
                topLeft = [i,j]
                flag = True
                break
        if flag:
            break
    ans = abs(3-topLeft[0]) + abs(1-topLeft[1])
    return ans



def get_successors(state):
    zero1 = None
    zero2 = None
    successors = set()
    for i in range(5):
        for j in range(4):
            if state.T[i][j] == 0:
                if(zero1 == None):
                    zero1 = [i,j]
                else:
                    zero2 = [i,j]

    # print(zero1)
    # print(zero2)
    #check if there are single pieces around both spaces that can be moved into the space
    #move a piece right
    if zero1[1] != 0 and state.T[zero1[0]][zero1[1]-1] == 7:
        puzzle = State(state.T,state,state.cost)
        puzzle.T[zero1[0]][zero1[1]] = 7
        puzzle.T[zero1[0]][zero1[1]-1] = 0
        successors.add(puzzle)
        # print("right")
        # print(state.T)

    if zero2[1] != 0 and state.T[zero2[0]][zero2[1]-1] == 7:
        puzzle = State(state.T,state,state.cost)
        puzzle.T[zero2[0]][zero2[1]] = 7
        puzzle.T[zero2[0]][zero2[1]-1] = 0
        successors.add(puzzle)
        # print("right2")

    #move a piece left
    if zero1[1] != 3 and state.T[zero1[0]][zero1[1]+1] == 7:
        puzzle = State(state.T,state,state.cost)
        puzzle.T[zero1[0]][zero1[1]] = 7
        puzzle.T[zero1[0]][zero1[1]+1] = 0
        successors.add(puzzle)

    if zero2[1] != 3 and state.T[zero2[0]][zero2[1]+1] == 7:
        puzzle = State(state.T,state,state.cost)
        puzzle.T[zero2[0]][zero2[1]] = 7
        puzzle.T[zero2[0]][zero2[1]+1] = 0
        successors.add(puzzle)

    #move a piece up
    if zero1[0] != 4 and state.T[zero1[0]+1][zero1[1]] == 7:
        puzzle = State(state.T,state,state.cost)
        puzzle.T[zero1[0]][zero1[1]] = 7
        puzzle.T[zero1[0]+1][zero1[1]] = 0
        successors.add(puzzle)

    if zero2[0] != 4 and state.T[zero2[0]+1][zero2[1]] == 7:
        puzzle = State(state.T,state,state.cost)
        puzzle.T[zero2[0]][zero2[1]] = 7
        puzzle.T[zero2[0]+1][zero2[1]] = 0
        successors.add(puzzle)

    #first move a piece down
    if zero1[0] != 0 and state.T[zero1[0]-1][zero1[1]] == 7:
        puzzle = State(state.T,state,state.cost)
        puzzle.T[zero1[0]][zero1[1]] = 7
        puzzle.T[zero1[0]-1][zero1[1]] = 0
        successors.add(puzzle)

    if zero2[0] != 0 and state.T[zero2[0]-1][zero2[1]] == 7:
        puzzle = State(state.T,state,state.cost)
        puzzle.T[zero2[0]][zero2[1]] = 7
        puzzle.T[zero2[0]-1][zero2[1]] = 0
        successors.add(puzzle)

    #now all the single pieces are done, move the 1*2 pieces
    #move vertical pieces right
    if zero1[1] == zero2[1] and (zero1[0] == zero2[0]+1 or zero1[0] == zero2[0]-1) and zero1[1] != 0:
        if (state.T[zero1[0]][zero1[1]-1] == state.T[zero2[0]][zero2[1]-1]) and state.T[zero1[0]][zero1[1]-1] != 7:
            puzzle = State(state.T,state,state.cost)
            puzzle.T[zero1[0]][zero1[1]] = puzzle.T[zero1[0]][zero1[1]-1]
            puzzle.T[zero2[0]][zero2[1]] = puzzle.T[zero2[0]][zero2[1]-1]
            if state.T[zero1[0]][zero1[1]-1] == 1:
                puzzle.T[zero1[0]][zero1[1]-2] = 0
                puzzle.T[zero2[0]][zero2[1]-2] = 0
            else:
                puzzle.T[zero1[0]][zero1[1]-1] = 0
                puzzle.T[zero2[0]][zero2[1]-1] = 0
            successors.add(puzzle)

    #move vertical pieces left
    if zero1[1] == zero2[1] and (zero1[0] == zero2[0]+1 or zero1[0] == zero2[0]-1) and zero1[1] != 3:
        if state.T[zero1[0]][zero1[1]+1] == state.T[zero2[0]][zero2[1]+1] and state.T[zero1[0]][zero1[1]+1] != 7:
            puzzle = State(state.T,state,state.cost)
            puzzle.T[zero1[0]][zero1[1]] = puzzle.T[zero1[0]][zero1[1]+1]
            puzzle.T[zero2[0]][zero2[1]] = puzzle.T[zero2[0]][zero2[1]+1]
            if state.T[zero1[0]][zero1[1]+1] == 1:
                puzzle.T[zero1[0]][zero1[1]+2] = 0
                puzzle.T[zero2[0]][zero2[1]+2] = 0
            else:
                puzzle.T[zero1[0]][zero1[1]+1] = 0
                puzzle.T[zero2[0]][zero2[1]+1] = 0
            successors.add(puzzle)

    #move horizontal pieces up
    if zero1[0] == zero2[0] and (zero1[1] == zero2[1]+1 or zero1[1] == zero2[1]-1) and zero1[0] != 4:
        if state.T[zero1[0]+1][zero1[1]] == state.T[zero2[0]+1][zero2[1]] and state.T[zero1[0]+1][zero1[1]] != 7:
            puzzle = State(state.T,state,state.cost)
            puzzle.T[zero1[0]][zero1[1]] = puzzle.T[zero1[0]+1][zero1[1]]
            puzzle.T[zero2[0]][zero2[1]] = puzzle.T[zero2[0]+1][zero2[1]]
            if state.T[zero1[0]+1][zero1[1]] == 1:
                puzzle.T[zero1[0]+2][zero1[1]] = 0
                puzzle.T[zero2[0]+2][zero2[1]] = 0
            else:
                puzzle.T[zero1[0]+1][zero1[1]] = 0
                puzzle.T[zero2[0]+1][zero2[1]] = 0
            successors.add(puzzle)

    #move horizontal pieces down
    if zero1[0] == zero2[0] and (zero1[1] == zero2[1]+1 or zero1[1] == zero2[1]-1) and zero1[0] != 0:
        if state.T[zero1[0]-1][zero1[1]] == state.T[zero2[0]-1][zero2[1]] and state.T[zero1[0]-1][zero1[1]] != 7:
            puzzle = State(state.T,state,state.cost)
            puzzle.T[zero1[0]][zero1[1]] = puzzle.T[zero1[0]-1][zero1[1]]
            puzzle.T[zero2[0]][zero2[1]] = puzzle.T[zero2[0]-1][zero2[1]]
            if state.T[zero1[0]-1][zero1[1]] == 1:
                puzzle.T[zero1[0]-2][zero1[1]] = 0
                puzzle.T[zero2[0]-2][zero2[1]] = 0
            else:
                puzzle.T[zero1[0]-1][zero1[1]] = 0
                puzzle.T[zero2[0]-1][zero2[1]] = 0
            successors.add(puzzle)

    #move horizontal piece right
    if zero1[1] > 1:
        if state.T[zero1[0]][zero1[1]-1] == state.T[zero1[0]][zero1[1]-2] and state.T[zero1[0]][zero1[1]-1] != 7 and state.T[zero1[0]][zero1[1]-1] != 1:
            puzzle = State(state.T,state,state.cost)
            puzzle.T[zero1[0]][zero1[1]] = puzzle.T[zero1[0]][zero1[1]-1]
            puzzle.T[zero1[0]][zero1[1]-2] = 0
            successors.add(puzzle)

    if zero2[1] > 1:
        if state.T[zero2[0]][zero2[1]-1] == state.T[zero2[0]][zero2[1]-2] and state.T[zero2[0]][zero2[1]-1] != 7 and state.T[zero2[0]][zero2[1]-1] != 1:
            puzzle = State(state.T,state,state.cost)
            puzzle.T[zero2[0]][zero2[1]] = puzzle.T[zero2[0]][zero2[1]-1]
            puzzle.T[zero2[0]][zero2[1]-2] = 0
            successors.add(puzzle)

    #move horizontal piece left
    if zero1[1] < 2:
        if state.T[zero1[0]][zero1[1]+1] == state.T[zero1[0]][zero1[1]+2] and state.T[zero1[0]][zero1[1]+1] != 7 and state.T[zero1[0]][zero1[1]+1] != 1:
            puzzle = State(state.T,state,state.cost)
            puzzle.T[zero1[0]][zero1[1]] = puzzle.T[zero1[0]][zero1[1]+1]
            puzzle.T[zero1[0]][zero1[1]+2] = 0
            successors.add(puzzle)

    if zero2[1] < 2:
        if state.T[zero2[0]][zero2[1]+1] == state.T[zero2[0]][zero2[1]+2] and state.T[zero2[0]][zero2[1]+1] != 7 and state.T[zero2[0]][zero2[1]+1] != 1:
            puzzle = State(state.T,state,state.cost)
            puzzle.T[zero2[0]][zero2[1]] = puzzle.T[zero2[0]][zero2[1]+1]
            puzzle.T[zero2[0]][zero2[1]+2] = 0
            successors.add(puzzle)

    #move vertical piece up
    if zero1[0] < 3:
        if state.T[zero1[0]+1][zero1[1]] == state.T[zero1[0]+2][zero1[1]] and state.T[zero1[0]+1][zero1[1]] != 7 and state.T[zero1[0]+1][zero1[1]] != 1:
            puzzle = State(state.T,state,state.cost)
            puzzle.T[zero1[0]][zero1[1]] = puzzle.T[zero1[0]+1][zero1[1]]
            puzzle.T[zero1[0]+2][zero1[1]] = 0
            successors.add(puzzle)

    if zero2[0] < 3:
        if state.T[zero2[0]+1][zero2[1]] == state.T[zero2[0]+2][zero2[1]] and state.T[zero2[0]+1][zero2[1]] != 7 and state.T[zero2[0]+1][zero2[1]] != 1:
            puzzle = State(state.T,state,state.cost)
            puzzle.T[zero2[0]][zero2[1]] = puzzle.T[zero2[0]+1][zero2[1]]
            puzzle.T[zero2[0]+2][zero2[1]] = 0
            successors.add(puzzle)

    #move vertical piece down
    if zero1[0] > 1:
        if state.T[zero1[0]-1][zero1[1]] == state.T[zero1[0]-2][zero1[1]] and state.T[zero1[0]-1][zero1[1]] != 7 and state.T[zero1[0]-1][zero1[1]] != 1:
            puzzle = State(state.T,state,state.cost)
            puzzle.T[zero1[0]][zero1[1]] = puzzle.T[zero1[0]-1][zero1[1]]
            puzzle.T[zero1[0]-2][zero1[1]] = 0
            successors.add(puzzle)

    if zero2[0] > 1:
        if state.T[zero2[0]-1][zero2[1]] == state.T[zero2[0]-2][zero2[1]] and state.T[zero2[0]-1][zero2[1]] != 7 and state.T[zero2[0]-1][zero2[1]] != 1:
            puzzle = State(state.T,state,state.cost)
            puzzle.T[zero2[0]][zero2[1]] = puzzle.T[zero2[0]-1][zero2[1]]
            puzzle.T[zero2[0]-2][zero2[1]] = 0
            successors.add(puzzle)

    # for successor in successors:
    #     print(successor.T)
    return successors


def a_star(initial_state):
    frontier = PQ()
    extended = 0
    generated = 0
    frontier.put((get_heuristic(initial_state), initial_state))
    visited = set()
    visited.add(initial_state.toString())
    while frontier.qsize() != 0:
        cur = frontier.get()[1]
        extended +=1
        # print(index)
        # print(cur)
        successors = get_successors(cur)
        for s in successors:
            if is_goal(s): 
                output(initial_state, s, generated, extended)
                return s
            priority = get_heuristic(s)+s.cost
            # print(priority)
            if s.toString() not in visited:
                generated += 1
                frontier.put((priority,s))
                visited.add(s.toString())
    return 


def bfs(initial_state):
    frontier = queue.Queue()
    extended = 0
    generated = 0
    frontier.put(initial_state)
    visited = set()
    visited.add(initial_state.toString())
    while frontier.qsize() != 0:
        cur = frontier.get()
        extended +=1
        # print(index)
        # print(cur)
        successors = get_successors(cur)
        for s in successors:
            if is_goal(s): 
                output(initial_state, s, generated, extended)
                return s
            priority = get_heuristic(s)+s.cost
            # print(priority)
            if s.toString() not in visited:
                generated += 1
                frontier.put(s)
                visited.add(s.toString())
    return


def dfs(initial_state):
    frontier = queue.LifoQueue()
    extended = 0
    generated = 0
    frontier.put(initial_state)
    visited = set()
    visited.add(initial_state.toString())
    while frontier.qsize() != 0:
        cur = frontier.get()
        extended +=1
        # print(index)
        # print(cur)
        successors = get_successors(cur)
        for s in successors:
            if is_goal(s): 
                output(initial_state, s, generated, extended)
                return s
            priority = get_heuristic(s)+s.cost
            # print(priority)
            if s.toString() not in visited:
                generated += 1
                frontier.put(s)
                visited.add(s.toString())
    return


def output(init, final, generated, expanded):
    if int(sys.argv[2]) == 1:
        if int(sys.argv[1]) == 1:
            f = open("puzzle1sol_astar.txt ", "w")
        else:
            f = open("puzzle2sol_astar.txt ", "w")
        f.write("ASTAR\n")
    elif int(sys.argv[2]) == 2:
        if int(sys.argv[1]) == 1:
            f = open("puzzle1sol_bfs.txt ", "w")
        else:
            f = open("puzzle2sol_bfs.txt ", "w")
        f.write("BFS\n")
    else:
        if int(sys.argv[1]) == 1:
            f = open("puzzle1sol_dfs.txt ", "w")
        else:
            f = open("puzzle2sol_dfs.txt ", "w")
        f.write("DFS\n")
    f.write("Initial state:\n")
    f.write(init.toOutput())
    f.write("\n\n"+"Cost of the (optimal) solution: "+str(final.cost)+"\n")
    f.write("Number of states expanded: "+str(expanded)+"\n")
    f.write("Number of stated generated: "+ str(generated)+"\n")
    f.write("\n"+"(Optimal) solution:"+"\n\n")
    path = []
    cost = final.cost
    while final.cost != 0:
        path+=[final.toOutput()]
        final = final.parent
    path+=[final.toOutput()]
    
    i = 0
    while i < cost+1:
        f.write(str(i)+"\n")
        f.write(path[cost-i]+"\n")
        i+=1
    # print(path)
    

    f.close()

if len(sys.argv) == 3:
    init = read_puzzle(int(sys.argv[1]))
    # print(init.toOutput())
    if int(sys.argv[2]) == 1:
        ans = a_star(init)
    elif int(sys.argv[2]) == 2:
        ans = bfs(init)
    elif int(sys.argv[2]) == 3:
        ans = dfs(init)


# print(init.T)
# print(ans.cost)

# test1 = State([[2,1,1,3],[2,1,1,3],[4,6,6,5],[4,7,7,5],[7,0,0,7]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],-1)
# get_successors(test1)

# test2 = State([[2, 1, 1, 3], [2, 1, 1, 3], [4, 6, 6, 5], [4, 7, 0, 5], [7, 0, 7, 7]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],2)
# get_successors(test2)

# test3 = State([[2, 1, 1, 3], [2, 1, 1, 3], [4, 6, 6, 5], [4, 0, 0, 5], [7, 7, 7, 7]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],2)
# get_successors(test3)

# test4 = State([[2, 1, 1, 3], [2, 1, 1, 3], [4, 0, 0, 5], [4, 6, 6, 5], [7, 7, 7, 7]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],2)
# get_successors(test4)

# test5 = State([[2, 1, 1, 3], [2, 1, 1, 3], [4, 0, 5, 7], [4, 0, 5, 7], [6, 6, 7, 7]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],2)
# get_successors(test5)

# test6 = State([[0, 1, 1, 3], [0, 1, 1, 3], [4, 2, 5, 7], [4, 2, 5, 7], [6, 6, 7, 7]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],2)
# get_successors(test6)

# test7 = State([[0, 1, 1, 3], [4, 1, 1, 3], [4, 2, 5, 7], [0, 2, 5, 7], [6, 6, 7, 7]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],2)
# get_successors(test7)

# test8 = State([[2, 1, 1, 3], [2, 1, 1, 3], [0, 6, 6, 0], [4,7,7,5], [4,7,7,5]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],2)
# get_successors(test8)

# test9 = State([[2, 3, 1, 1], [2, 3, 1, 1], [0, 6, 6, 0], [4,7,7,5], [4,7,7,5]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],2)
# print(get_heuristic(test9))

# test1 = State([[2,6,6,3],[2,7,4,3],[1,1,4,5],[1,1,7,5],[7,0,0,7]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],-1)
# test2 = State([[2,4,5,3],[2,4,5,3],[6,6,7,7],[1,1,0,7],[1,1,0,7]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],-1)

# get_successors(test2)

# ans = a_star(test1)
# print(ans.cost)

# read_puzzle(1)

