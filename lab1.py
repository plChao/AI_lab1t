#!/usr/bin/python
# -*- coding: UTF-8 -*-
# -*- coding: utf-8 -*-
import time
import random
import datetime
maxlenofdic = 16
maxgoingnode = 200*10000
tStart = time.time()                                                       #計時開始
print(datetime.datetime.now().time())
def copyr(relations):
    copyrela = []
    for x in relations:
        copyrela.append(cord(x.x,x.y))
    return copyrela
def copya(assignments):
    copyas = []
    for x in assignments:
        copyas.append(anspair(x.puzzlenum,x.ans))
    return copyas
class anspair:
    def __init__(self, puzzlenum, ans):
        self.puzzlenum = int(puzzlenum)
        self.ans = ans
    def __repr__(self):
        return "("+str(self.puzzlenum)+","+self.ans+")"
class status:
    def __init__(self, puzzles, assignments = []):
        self.puzzles = puzzles
        self.assignments = []
    #def showpuzzle():
    def copyn(self):
        puzzlecopy = []
        for x in self.puzzles:
            puzzlecopy.append(puzzle(x.cord.x,x.cord.y,x.lens,x.direction, \
                x.boundary.copy(),x.num))
            puzzlecopy[len(puzzlecopy)-1].relations = copyr(x.relations)
            puzzlecopy[len(puzzlecopy)-1].relationum = x.relationum
        return puzzlecopy

    def getpuzzle(self, num):
        for x in self.puzzles:
            if x.num == num:
                return x
        print("error: non puzzle")
        print(num)
    def print(self):
        '''
        print("puzzles")
        for x in self.puzzles:
            print(x.cord)
            print(x.lens)
            print(x.direction)
            print(x.num)
            print(len(x.boundary))
            print(x.boundary)
            print(x.relations)
            print(x.relationum)
            print("-------------------")
        '''
        #print("anser")
        print(self.assignments)
    def puzzlesSort(self, MRV, DegreeH,Random):
        puzzlecopy = self.puzzles.copy()
        if Random:
            random.shuffle(puzzlecopy)
        if MRV == 1 and DegreeH ==1 :
            puzzlecopy = sorted(puzzlecopy)
        elif MRV == 1 and DegreeH ==0 :
            puzzlecopy = sorted(puzzlecopy, key = lambda x : len(x.boundary))
        elif MRV == 0 and DegreeH ==1 :
            puzzlecopy = sorted(puzzlecopy, key = lambda x : x.relationum, reverse = True)
        #test = status(puzzlecopy)
        #test.print()
        return puzzlecopy
    def constAC3Reboun(self, puzzlef):
        stack = []
        stack.append(self.getpuzzle(puzzlef.num))
        newbound = []
        while len(stack)!=0:
            puzzle = stack.pop()
            #print(puzzle.boundary)
            for x in range(0,len(puzzle.relations)):
                if puzzle.relations[x].x != -1 :
                    newbound.clear()
                    target = self.getpuzzle(x)
                    #print(puzzle.relations[x])
                    if puzzle.direction == 'A' :
                        crossletter = set()
                        for y in puzzle.boundary:
                            crossletter.add(y[puzzle.relations[x].x-puzzle.cord.x])
                        #print(crossletter)
                        position = puzzle.relations[x].y - target.cord.y
                        #print(position)
                        for y in target.boundary:
                            if y[position] in crossletter:
                                newbound.append(y)
                        if target.boundary != newbound:
                            target.boundary = newbound.copy()
                            stack.append(target)
                    else :
                        #print(puzzle.relations[x].y - puzzle.cord.y)
                        crossletter = set()
                        for y in puzzle.boundary:
                            crossletter.add(y[puzzle.relations[x].y - puzzle.cord.y])
                        #print(crossletter)
                        position = puzzle.relations[x].x - target.cord.x
                        #print(position)
                        for y in target.boundary:
                            if y[position] in crossletter:
                                newbound.append(y)
                        if target.boundary != newbound:
                            target.boundary = newbound.copy()
                            stack.append(target)
                    #print(self.puzzles[x].boundary)

    def constReBound(self, puzzle, value) :
        newbound = []
        #print(value)
        for x in range(0,len(puzzle.relations)) :
            if puzzle.relations[x].x != -1 :
                newbound.clear()
                target = self.getpuzzle(x)
                #print(puzzle.relations[x])
                if puzzle.direction == 'A' :
                    #print(puzzle.relations[x].y - puzzle.cord.y)
                    crossletter = value[puzzle.relations[x].x-puzzle.cord.x]
                    #print(crossletter)
                    position = puzzle.relations[x].y - target.cord.y
                    #print(position)
                    for y in target.boundary:
                        if y[position] == crossletter:
                            newbound.append(y)
                    target.boundary = newbound.copy()
                else :
                    #print(puzzle.relations[x].y - puzzle.cord.y)
                    crossletter = value[puzzle.relations[x].y - puzzle.cord.y]
                    #print(crossletter)
                    position = puzzle.relations[x].x - target.cord.x
                    #print(position)
                    for y in target.boundary:
                        if y[position] == crossletter:
                            newbound.append(y)
                    target.boundary = newbound.copy()
                #print(self.puzzles[x].boundary)

    def constrain(self, puzzle, value) :
        ans = 0
        for x in range(0,len(puzzle.relations)) :
            if puzzle.relations[x].x != -1 :
                #print(puzzle.relations[x])
                target = self.getpuzzle(x)
                if puzzle.direction == 'A' :
                    crossletter = value[puzzle.relations[x].x-puzzle.cord.x]
                    position =  puzzle.relations[x].y - target.cord.y
                    for y in target.boundary:
                        if y[position] != crossletter:
                            ans += 1
                else :
                    crossletter = value[puzzle.relations[x].y - puzzle.cord.y]
                    #print(crossletter)
                    position = puzzle.relations[x].x - target.cord.x
                    #print(position)
                    #print(target.boundary)
                    for y in target.boundary:
                        if y[position] != crossletter:
                            ans += 1
        return ans
    def getanswer(self):
        for x in self.puzzles:
            if len(x.boundary) == 0:
                return False
        return True
    def success(self):
        if len(self.assignments) == len(self.puzzles) :
            #print("success!!!")
            return True
        return False

class cord:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
    def sub(self, cord2):
        x = self.x - cord2.x
        y = self.y - cord2.y
        return cord(x,y)
    def __repr__(self):
        return "("+str(self.x)+","+str(self.y)+")"

class puzzle:
    def __init__(self, x, y, lens, direction, boundary, num, relations = [], relationum = 0):
        self.cord = cord(x, y)
        self.lens = int(lens)
        self.direction = direction
        self.boundary = boundary
        self.relations = []
        self.relationum = 0
        self.num = num

    def relation(self, block):
        if self == block :
            ans = cord(-1,-1)
            return ans;
        elif block.direction == self.direction :
            ans = cord(-1,-1)
            return ans;
        elif self.direction == 'A' :
            if self.cord.y >= block.cord.y and self.cord.y <= (block.cord.y+block.lens-1) and \
            block.cord.x >= self.cord.x and block.cord.x <= (self.cord.x+self.lens-1) :
                ans = cord(block.cord.x,self.cord.y)
                return ans;
            else :
                ans = cord(-1,-1)
                return ans;
        else:
            if block.cord.y >= self.cord.y and block.cord.y <= (self.cord.y+self.lens-1) and \
            self.cord.x >= block.cord.x and self.cord.x <= (block.cord.x+block.lens-1) :
                ans = cord(self.cord.x,block.cord.y)
                return ans;
            else :
                ans = cord(-1,-1)
                return ans;
    def __lt__(x, y):
        if len(x.boundary) == len(y.boundary):
            return y.relationum < x.relationum
        else:
            return len(x.boundary) < len(y.boundary)
    def __eq__(x, y):
        return x.num == y.num

def DFS(node, MRV, DegreeH, LCV, AC3, Random):
    #node.print()
    global nodevisit
    global forward
    global maxgoingnode
    if len(node.assignments) == len(node.puzzles) :
        #print("success!!!")
        return node
    for x in node.puzzles:
        if len(x.boundary) == 0:
            #print("failded QQ")
            return node

    mini = 3000*len(node.puzzles)
    # MRV,DegreeH

    order = node.puzzlesSort(MRV,DegreeH,Random)
    #node.print()
    #test = status(order)
    #test.print()
    #LCV
    for target in order :
        if len(target.boundary) == 1:
            continue
        #print(target.num)
        #print("layer" + str(layer))
        #test = status(order)
        #test.print()
        #print(target.boundary)
        if Random :
            random.shuffle(target.boundary)
        if LCV :
            target.boundary = sorted(target.boundary, key = lambda x : node.constrain(target,x), reverse = False)
        #print(target.boundary)
        for y in target.boundary:
            #print(len(target.boundary))
            #print(y)
            #puzzlecopy = copy.deepcopy(node.puzzles)
            puzzlecopy = node.copyn()
            childnode = status(puzzlecopy)

            nodevisit+=1
            if(nodevisit > maxgoingnode):
                return node

            childnode.getpuzzle(target.num).boundary.clear()
            childnode.getpuzzle(target.num).boundary.append(y)

            if AC3:
                #print("AC3 "+str(target.num))
                childnode.constAC3Reboun(target)
                #print("endAC3")
                #childnode.print()
            else:
                childnode.constReBound(target,y)
            if not childnode.getanswer() :           #forword cheaking
                #print("cheak this ganna filed")
                forward += 1
                childnode.puzzles.clear()
                childnode.assignments.clear()
                continue


            decide = anspair(target.num,y)
            #print(decide)
            childnode.assignments = copya(node.assignments)
            childnode.assignments.append(decide)
            #print("childnode")
            #childnode.print()
            #print("node")
            #node.print()
            terminalnode = DFS(childnode,MRV,DegreeH,LCV,AC3,Random)
            if terminalnode.success():
                return terminalnode

    #print("re node")
    return node


def solve(graphli,dictionary, MRV = False, DegreeH = False,LCV = False, AC3 = True, Random = False):
    blocks = []
    for x in graphli :                                                          # read blocks and initialize puzzles
        x = x.replace('\n', '')
        tmp = x.split(" ")
        blocks.append(puzzle(tmp[0],tmp[1],tmp[2],tmp[3], \
            dictionary[int(tmp[2])], len(blocks)))
    for x in blocks :                                                           # initilize the binary relation
        for y in blocks :
            no_relation = cord(-1,-1)
            tmp2 = x.relation(y)
            x.relations.append(tmp2)
            if tmp2.x != -1:
                x.relationum +=1

    root = status(blocks)
    ans = DFS(root,MRV,DegreeH,LCV,AC3,Random)
    print("MRV:" +str(MRV)+" Degree:" + str(DegreeH)+" LCV:"+str(LCV)+" AC3:"+str(AC3)+" Random:"+str(Random))
    ans.print()
    print("visited nodes "+str(nodevisit))
    print("forward checking "+str(forward))



#open dictionary, the max len in dic is 14

words = open("English words 3000.txt", "r")
strw = words.read()
listw = strw.split("\n")
words.close()

# sort as length
dictionary = []
for x in range(0,maxlenofdic) :
    subdic = []
    dictionary.append(subdic)
for x in listw :
    dictionary[len(x)].append(x)

# get question
puzzle_f = open("puzzle.txt", "r")
question = puzzle_f.readlines()

# solve
nodevisit = 0
forward = 0
for x in range(3,4) :
    graph = question[x].split("   ")
    solve(graph, dictionary)
    nodevisit = 0
    forward = 0



#for x in listw :

tEnd = time.time()#計時結束

print("It cost %f sec"% (tEnd - tStart))#會自動做近位
#print tEnd - tStart#原型長這樣
