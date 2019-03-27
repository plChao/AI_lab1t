#!/usr/bin/python
# -*- coding: UTF-8 -*-
class cord:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

class puzzle:
    def __init__(self, x, y, lens, direction):
        self.cord = cord(x, y)
        self.lens = int(lens)
        self.direction = direction

    def relation(self, block):
        if block.direction == self.direction :
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



def solve(graphli):
    blocks = []
    for x in graphli :
        tmp = x.split(" ")
        blocks.append(puzzle(tmp[0],tmp[1],tmp[2],tmp[3]))

    re = blocks[0].relation(blocks[2])
    print(re.x)

#open dictionary
'''
words = open("English words 3000.txt", "r")
strw = words.read()
listw = strw.split("\n")
words.close()
'''
puzzle_f = open("puzzle.txt", "r")
question = puzzle_f.readlines()
for x in range(0,1) :
    graph = question[x].split("   ")
    solve(graph)




#for x in listw :


