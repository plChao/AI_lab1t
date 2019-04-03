#!/usr/bin/python
# -*- coding: UTF-8 -*-
# -*- coding: utf-8 -*-
import numpy as np
import time
maxlenofdic = 16
tStart = time.time()                                                            #計時開始

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
            #print(x.boundary)
            #print [cord.x for cord in x.relations]
            print(x.relations)
            print(x.relationum)
            print("-------------------")
        print("anser")
        print(self.assignments)
    def MRV(self):                                                              #Minimum remaining values heuristic
        mini = 3000
        for x in self.puzzles:
            if mini > len(x.boundary) :
                mini = len(x.boundary)
                ans = x
        return ans
    def DegreeH(self):                                                          #Degree heuristic
        maxi = 0
        for x in self.puzzles:
            if maxi < len(x.relations) :
                maxi = len(x.relations)
                ans = x
        return ans
    def LCV(self, puzzle):                                                      #Least constraining value heuristic
        mini = 3000*len(self.puzzles)
        for x in puzzle.boundary:
            tmp = self.constrain(puzzle,x)
            if mini > tmp:
                mini = tmp
                ans = x
        return ans
    def constrain(self, puzzle, value) :
        ans = 0
        for x in range(0,len(puzzle.relations)) :
            if puzzle.relations[x].x != -1 :
                if puzzle.direction == 'A' :
                    crossletter = value[puzzle.relations[x].x-puzzle.cord.x]
                    position = puzzles[x].cord.y - puzzle.relations[x].y
                    for y in puzzles[x].boundary:
                        if y[position] != crossletter:
                            ans += 1
                else :
                    crossletter = value[puzzle.cord.y - puzzle.relations[x].y]
                    position = puzzle.relations[x].x - puzzles[x].cord.x
                    for y in puzzles[x].boundary:
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
    def __init__(self, x, y, lens, direction, boundary, relations = [], relationum = 0):
        self.cord = cord(x, y)
        self.lens = int(lens)
        self.direction = direction
        self.boundary = boundary
        self.relations = []
        self.relationum = 0

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
    def boundCondNum(self, word, position):
        ans = 0
        for x in self.boundary :
            if x[position] == word :
                ans+=1
        return ans





def DFS(status, MRV, DegreeH, LCV, AC3):
    print(1)



def solve(graphli,dictionary):
    blocks = []
    for x in graphli :                                                          # read blocks and initialize puzzles
        x = x.replace('\n', '')
        tmp = x.split(" ")
        blocks.append(puzzle(tmp[0],tmp[1],tmp[2],tmp[3], \
            dictionary[int(tmp[2])]))
    for x in blocks :                                                           # initilize the binary relation
        for y in blocks :
            no_relation = cord(-1,-1)
            tmp2 = x.relation(y)
            x.relations.append(tmp2)
            if tmp2.x != -1:
                x.relationum +=1

    root = status(blocks)
    root.print()
    ans = DFS(root,1,1,1,1)






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
