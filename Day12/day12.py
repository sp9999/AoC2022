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
    def __init__(self, lines):
        self.grid = []
        self.maxY = len(lines)
        self.maxX = len(lines[0])
        self.startList = []
        for y in range(0, self.maxY):
            self.grid.append([])
            for x in range(0, self.maxX):
                c = lines[y][x]
                if c == "S":
                    self.start = (y, x)
                    self.grid[y].append(0)
                    self.startList.append((y, x))
                elif c == "E":
                    self.goal = (y, x)
                    self.grid[y].append(26)
                else:
                    self.grid[y].append(int(ord(c) - ord('a')))
                    if c == 'a':
                        self.startList.append((y, x))

    def print(self):
        for y in range(0, self.maxY):
            print(self.grid[y])
        print("\n")

    def reconstructPath(self, cameFrom, current):
        path = [current]
        while current in cameFrom:
            current = cameFrom[current]
            path.insert(0, current)
        return path

    def calcDistSquared(self, curr):
        dy = abs(curr[0] - self.goal[0])
        dx = abs(curr[1] - self.goal[1])
        return dx * dx + dy * dy

    def aStar(self, start):
        openSet = set()
        openSet.add(start)
        cameFrom = {}

        gScore = {}
        gScore[start] = 0

        fScore = {}
        fScore[start] = self.calcDistSquared(start)

        while len(openSet) > 0:
            curr = openSet.pop()
            if curr == self.goal:
                return self.reconstructPath(cameFrom, curr)

            currY = curr[0]
            currX = curr[1]
            currVal = self.get(currY, currX)
            neighbors = self.getNeighbors(currY, currX, currVal)
            for n in neighbors:
                tempScore = gScore[curr] + 1
                neighborScore = gScore.get(n)
                if neighborScore is None or tempScore < neighborScore:
                    cameFrom[n] = curr
                    gScore[n] = tempScore
                    fScore[n] = tempScore + self.calcDistSquared(n)
                    if n not in openSet:
                        openSet.add(n)

        return None

    def aStarList(self):
        lengths = []
        for start in self.startList:
            path = self.aStar(start)
            if path is not None:
                lengths.append(len(path))
        lengths.sort()
        return lengths[0] - 1

    def get(self, y, x):
        return self.grid[y][x]

    def getNeighbors(self, y, x, val, allowDiagonals=False):
        potentialNeighbor = []
        if y > 0:
            if x >= 0 and allowDiagonals:
                if self.get(y - 1, x - 1) <= val + 1:
                    potentialNeighbor.append((y - 1, x - 1))
            if self.get(y - 1, x) <= val + 1:
                potentialNeighbor.append((y - 1, x))
            if x < (self.maxX - 1) and allowDiagonals:
                if self.get(y - 1, x + 1) <= val + 1:
                    potentialNeighbor.append((y - 1, x + 1))

        if x > 0:
            if self.get(y, x - 1) <= val + 1:
                potentialNeighbor.append((y, x - 1))
        if x < (self.maxX - 1):
            if self.get(y, x + 1) <= val + 1:
                potentialNeighbor.append((y, x + 1))

        if y < (self.maxY - 1):
            if x >= 0 and allowDiagonals:
                if self.get(y + 1, x - 1) <= val + 1:
                    potentialNeighbor.append((y + 1, x - 1))
            if self.get(y + 1, x) <= val + 1:
                potentialNeighbor.append((y + 1, x))
            if x < (self.maxX - 1) and allowDiagonals:
                if self.get(y + 1, x + 1) <= val + 1:
                    potentialNeighbor.append((y + 1, x + 1))

        return potentialNeighbor


def puzzle(input, part2=False):
    g = Grid(input)
    if not part2:
        return len(g.aStar(g.start)) - 1
    else:
        g = Grid(input)
        return g.aStarList()

sp1 = puzzle(sample)
p1 = puzzle(lines)
sp2 = puzzle(sample, True)
p2 = puzzle(lines, True)

print("SP1: " + str(sp1))   # 31
print("SP2: " + str(sp2))   # 29
print("P1: " + str(p1))     # 484
print("P2: " + str(p2))     # 478

if p1 != 0 and submit(p1, part="a", day=DAY, year=YEAR) is None:
    if p2 != 0:
        submit(p2, part="b", day=DAY, year=YEAR)