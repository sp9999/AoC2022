import utility
import session
import os
import sys
from aocd.models import Puzzle
from aocd import submit
os.environ["AOC_SESSION"] = session.AOC_SESSION

DAY = int(sys.argv[0].rsplit('/', 1)[1][3:-3])
YEAR = int(sys.argv[0].rsplit('/', 3)[1])

## INPUT STUFF
puzzle = Puzzle(year=YEAR, day=DAY)
data = puzzle.input_data
lines = utility.inputDataToLines(data)

## SAMPLE INPUT STUFF
sample = []
with open("./input.txt", encoding="utf8") as fp:
    for line in fp:
        sample.append(line.strip())

## CONVERT INPUT STRING LIST TO NUMBERS IF POSSIBLE
try:
    nums = utility.listStringToListNum(lines)
    sampleNum = utility.listStringToListNum(sample)
except:
    nums = []
    sampleNum = []

sp1 = sp2 = p1 = p2 = 0

class Grid:
    def __init__(self, rows, cols, xAdjust, yAdjust, sandSpawn):
        self.m = [["." for y in range(rows)] for x in range(cols)]
        self.minX = cols
        self.maxX = 0
        self.minY = rows
        self.maxY = 0
        self.xAdjust = xAdjust
        self.yAdjust = yAdjust
        self.sandPlaced = 0
        newY = sandSpawn[1] + self.yAdjust
        newX = sandSpawn[0] + self.xAdjust
        self.sandSpawn = (newY, newX)
        self.m[newY][newX] = "+"
        if newY < self.minY:
            self.minY = newY
        if newY > self.maxY:
            self.maxY = newY

        if newX < self.minX:
            self.minX = newX
        if newX > self.maxX:
            self.maxX = newX

    def print(self):
        for y in range(self.minY - 1, self.maxY + 1):
            str = ""
            for x in range(self.minX - 1, self.maxX + 1):
                str += self.m[y][x]
            print(str)
        print("\n")

    def parseRocks(self, line):
        nodes = line.split(" -> ")
        for i in range(0, len(nodes) - 1):
            n0 = eval(nodes[i])
            n1 = eval(nodes[i+1])

            dx = n1[0] - n0[0]
            dy = n1[1] - n0[1]

            if dy == 0:
                adjust = int(dx / abs(dx))
                newY = n0[1] + self.yAdjust
                if newY < self.minY:
                    self.minY = newY
                if newY > self.maxY:
                    self.maxY = newY
                for x in range(n0[0], n1[0] + adjust, adjust):
                    newX = x + self.xAdjust
                    self.m[newY][newX] = "#"
                    if newX < self.minX:
                        self.minX = newX
                    if newX > self.maxX:
                        self.maxX = newX

            elif dx == 0:
                adjust = int(dy / abs(dy))
                newX = n0[0] + self.xAdjust
                if newX < self.minX:
                    self.minX = newX
                if newX > self.maxX:
                    self.maxX = newX
                for y in range (n0[1], n1[1] + adjust, adjust):
                    newY = y + self.yAdjust
                    self.m[newY][newX] = "#"
                    if newY < self.minY:
                        self.minY = newY
                    if newY > self.maxY:
                        self.maxY = newY


    def get(self, y, x):
        return self.m[y][x]

    def setSand(self, pos):
        self.m[pos[0]][pos[1]] = "O"

    def addSand(self, pos, part2):
        currY = pos[0]
        currX = pos[1]

        # go down until not air
        while self.get(currY + 1, currX) == ".":
            currY += 1
            if currY > self.maxY and part2 is False:
                return False

        while self.get(currY + 1, currX - 1) == ".":
            currY += 1
            currX -= 1
            return self.addSand((currY, currX), part2)
        while self.get(currY + 1, currX + 1) == ".":
            currY += 1
            currX += 1
            return self.addSand((currY, currX), part2)

        if part2 and (currY, currX) == self.sandSpawn:
            return False
        self.setSand((currY, currX))
        self.sandPlaced += 1
        return True





def puzzle(input, part2=False):
    result = 0
    grid = Grid(500, 500, -200, 1, (500, 0))
    for line in input:
        grid.parseRocks(line)
    if not part2:
        while grid.addSand(grid.sandSpawn, part2):
            result += 1
        grid.print()
    else:
        newMaxY = str(grid.maxY - grid.yAdjust + 2)
        bufferX = 150
        bottomLine = str(grid.minX - grid.xAdjust - bufferX) + "," + newMaxY + " -> " + str(grid.maxX - grid.xAdjust + bufferX) + "," + newMaxY
        grid.parseRocks(bottomLine)
        while grid.addSand(grid.sandSpawn, part2):
            result += 1
        grid.print()
        result += 1
    return result

sp1 = puzzle(sample)
p1 = puzzle(lines)
sp2 = puzzle(sample, True)
p2 = puzzle(lines, True)

print("SP1: " + str(sp1))   # 24
print("SP2: " + str(sp2))   # 93
print("P1: " + str(p1))     # 838
print("P2: " + str(p2))     # 27539

if p1 != 0 and submit(p1, part="a", day=DAY, year=YEAR) is None:
    if p2 != 0:
        submit(p2, part="b", day=DAY, year=YEAR)