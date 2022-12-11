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
    sampleNum = utility.listStringToListNum(sample)
    nums = utility.listStringToListNum(lines)
except:
    nums = []
    sampleNum = []

sp1 = sp2 = p1 = p2 = 0

def isVisible(input, y, x, maxY, maxX):
    currVal = input[y][x]
    # go up
    visible = True
    for i_y in range(y - 1, -1, -1):
        if currVal <= input[i_y][x]:
            visible = False
            break

    if visible:
        return True

    # down
    visible = True
    for i_y in range(y + 1, maxY):
        if currVal <= input[i_y][x]:
            visible = False
            break

    if visible:
        return True

    # left
    visible = True
    for i_x in range(x - 1, -1, -1):
        if currVal <= input[y][i_x]:
            visible = False
            break

    if visible:
        return True

    # right
    visible = True
    for i_x in range(x + 1, maxX):
        if currVal <= input[y][i_x]:
            visible = False
            break

    return visible

def calcScenicScore(input, y, x, maxY, maxX):
    currVal = input[y][x]
    # go up
    rangeVal = [0, 0, 0, 0]
    for i_y in range(y - 1, -1, -1):
        rangeVal[0] = rangeVal[0] + 1
        if currVal <= input[i_y][x]:
            break

    # down
    for i_y in range(y + 1, maxY):
        rangeVal[1] = rangeVal[1] + 1
        if currVal <= input[i_y][x]:
            break

    # left
    visible = True
    for i_x in range(x - 1, -1, -1):
        rangeVal[2] = rangeVal[2] + 1
        if currVal <= input[y][i_x]:
            break

    # right
    visible = True
    for i_x in range(x + 1, maxX):
        rangeVal[3] = rangeVal[3] + 1
        if currVal <= input[y][i_x]:
            break

    return rangeVal[0] * rangeVal[1] * rangeVal[2] * rangeVal[3]

def findVisibleTrees(input):
    maxY = len(input)
    maxX = len(input[0])
    numVisible = 2 * (maxX + maxY) - 4
    for y in range(1, len(input) - 1):
        for x in range(1, len(input[y]) - 1):
            if isVisible(input, y, x, maxY, maxX):
                numVisible += 1
    return numVisible

def findTreeHouse(input):
    maxY = len(input)
    maxX = len(input[0])
    maxScore = 0
    for y in range(1, len(input) - 1):
        for x in range(1, len(input[y]) - 1):
            score = calcScenicScore(input, y, x, maxY, maxX)
            if score > maxScore:
                maxScore = score
    return maxScore

def puzzle(input, part2=False):
    result = 0
    array = utility.inputDataToInt2DArray(input)
    if not part2:
        result = findVisibleTrees(array)
    else:
        result += findTreeHouse(input)
    return result

sp1 = puzzle(sample)        # 21
p1 = puzzle(lines)          # 1785
sp2 = puzzle(sample, True)  # 8
p2 = puzzle(lines, True)    # 345168

print("SP1: " + str(sp1))
print("SP2: " + str(sp2))
print("P1: " + str(p1))
print("P2: " + str(p2))

if p1 != 0 and submit(p1, part="a", day=DAY, year=YEAR) is None:
    if p2 != 0:
        submit(p2, part="b", day=DAY, year=YEAR)