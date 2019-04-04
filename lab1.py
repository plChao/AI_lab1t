#!/usr/bin/python
# -*- coding: UTF-8 -*-
# -*- coding: utf-8 -*-
import numpy as np
import time
import random
maxlenofdic = 16
tStart = time.time()                                                            #計時開始
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
    def print(self):
        print("puzzles")
        for x in self.puzzles:
            print(x.cord)
            print(x.lens)
            print(x.direction)
            print(x.num)
            print(len(x.boundary))
            #print(x.boundary)
            print(x.relations)
            print(x.relationum)
            print("-------------------")
        print("anser")
        print(self.assignments)
    def puzzlesSort(self, MRV, DegreeH):
        puzzlecopy = self.puzzles.copy()
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
    def constReBound(self, puzzle, value) :
        newbound = []
        for x in range(0,len(puzzle.relations)) :
            if puzzle.relations[x].x != -1 :
                print(puzzle.relations[x])
                if puzzle.direction == 'A' :
                    crossletter = value[puzzle.relations[x].x-puzzle.cord.x]
                    print(crossletter)
                    position = puzzle.relations[x].y - self.puzzles[x].cord.y
                    print(position)
                    for y in self.puzzles[x].boundary:
                        if y[position] == crossletter:
                            newbound.append(y)
                    print(x)
                    self.puzzles[x].boundary = newbound.copy()
                else :
                    print(puzzle.relations[x].x-puzzle.cord.x)
                    crossletter = value[puzzle.cord.y - puzzle.relations[x].y]
                    position = puzzle.relations[x].x - self.puzzles[x].cord.x
                    for y in self.puzzles[x].boundary:
                        if y[position] == crossletter:
                            newbound.append(y)
                    self.puzzles[x].boundary = newbound.copy()
                print(self.puzzles[x].boundary)

    def constrain(self, puzzle, value) :
        ans = 0
        for x in range(0,len(puzzle.relations)) :
            if puzzle.relations[x].x != -1 :
                if puzzle.direction == 'A' :
                    crossletter = value[puzzle.relations[x].x-puzzle.cord.x]
                    position =  puzzle.relations[x].y - self.puzzles[x].cord.y
                    for y in self.puzzles[x].boundary:
                        if y[position] != crossletter:
                            ans += 1
                else :
                    crossletter = value[puzzle.cord.y - puzzle.relations[x].y]
                    position = puzzle.relations[x].x - self.puzzles[x].cord.x
                    for y in self.puzzles[x].boundary:
                        if y[position] != crossletter:
                            ans += 1
        return ans


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



def DFS(node, MRV = 1, DegreeH = 1, LCV = 1, AC3 = 1):
    mini = 3000*len(node.puzzles)
    # MRV,DegreeH
    order = node.puzzlesSort(MRV,DegreeH)
    ans = []
    #LCV
    #for x in order :

    for y in order[0].boundary:
        tmp = node.constrain(order[0],y)
        if mini > tmp:
            mini = tmp
            ans.clear()
            ans.append(y)
        elif mini == tmp:
            ans.append(y)
    #random.shuffle(ans)
    # AC3
    puzzlecopy = node.puzzles.copy()
    childnode = status(puzzlecopy)

    childnode.print()

    childnode.constReBound(order[0],ans[0])

    childnode.print()

    childnode.puzzles.remove(order[0])
    decide = anspair(order[0].num,ans[0])
    childnode.assignments.append(decide)
    #DFS(childnode)



def solve(graphli,dictionary):
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

    ans = DFS(root)






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
for x in range(0,1) :
    graph = question[x].split("   ")
    solve(graph, dictionary)



#for x in listw :

tEnd = time.time()#計時結束

print("It cost %f sec"% (tEnd - tStart))#會自動做近位
#print tEnd - tStart#原型長這樣
