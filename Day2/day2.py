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

p1ResultMap = {
    "A": {"X": 3, "Y": 6, "Z": 0},
    "B": {"X": 0, "Y": 3, "Z": 6},
    "C": {"X": 6, "Y": 0, "Z": 3}
}

p1ShapeMap = {
    "A": {"X": 1, "Y": 2, "Z": 3},
    "B": {"X": 1, "Y": 2, "Z": 3},
    "C": {"X": 1, "Y": 2, "Z": 3}
}

p2ResultMap = {
    "A": {"X": 0, "Y": 3, "Z": 6},
    "B": {"X": 0, "Y": 3, "Z": 6},
    "C": {"X": 0, "Y": 3, "Z": 6}
}

p2ShapeMap = {
    "A": {"X": 3, "Y": 1, "Z": 2},
    "B": {"X": 1, "Y": 2, "Z": 3},
    "C": {"X": 2, "Y": 3, "Z": 1}
}


def RPS(elf, input, resultMap, shapeMap):
    return resultMap[elf][input] + shapeMap[elf][input]


def puzzle(input, part2=False):
    result = 0
    for line in input:
        elf, second = line.split(" ")
        if part2:
            roundResult = RPS(elf, second, p2ResultMap, p2ShapeMap)
        else:
            roundResult = RPS(elf, second, p1ResultMap, p1ShapeMap)
        result += roundResult
    return result

sp1 = puzzle(sample)
p1 = puzzle(lines)
sp2 = puzzle(sample, True)
p2 = puzzle(lines, True)

print("SP1: " + str(sp1))   # 15
print("SP2: " + str(sp2))   # 12
print("P1: " + str(p1))     # 14297
print("P2: " + str(p2))     # 10498

if p1 != 0 and submit(p1, part="a", day=DAY, year=YEAR) is None:
    if p2 != 0:
        submit(p2, part="b", day=DAY, year=YEAR)
