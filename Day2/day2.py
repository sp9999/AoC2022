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


def RPS(elf, input, part2):
    ROCK = "A"
    PAPER = "B"
    # SCISSORS = "C"
    ROCKORLOSE = "X"
    PAPERORDRAW = "Y"
    # SCISSORSORWIN = "Z"

    SHAPEVALUE = [0, 1, 2, 3]
    RESULTVALUE = [0, 3, 6]
    RESULT_LOSE = 0
    RESULT_DRAW = 1
    RESULT_WIN = 2

    if elf == ROCK:
        if input == ROCKORLOSE:
            if part2:
                return RESULTVALUE[RESULT_LOSE] + SHAPEVALUE[3]
            return RESULTVALUE[RESULT_DRAW] + SHAPEVALUE[1]
        elif input == PAPERORDRAW:
            if part2:
                return RESULTVALUE[RESULT_DRAW] + SHAPEVALUE[1]
            return RESULTVALUE[RESULT_WIN] + SHAPEVALUE[2]
        else: # input == SCISSORSORWIN
            if part2:
                return RESULTVALUE[RESULT_WIN] + SHAPEVALUE[2]
            return RESULTVALUE[RESULT_LOSE] + SHAPEVALUE[3]
    elif elf == PAPER:
        if input == ROCKORLOSE:
            return RESULTVALUE[RESULT_LOSE] + SHAPEVALUE[1]
        elif input == PAPERORDRAW:
            return RESULTVALUE[RESULT_DRAW] + SHAPEVALUE[2]
        else: # input == SCISSORSORWIN
            return RESULTVALUE[RESULT_WIN] + SHAPEVALUE[3]
    else: # SCISSORS
        if input == ROCKORLOSE:
            if part2:
                return RESULTVALUE[RESULT_LOSE] + SHAPEVALUE[2]
            return RESULTVALUE[RESULT_WIN] + SHAPEVALUE[1]
        elif input == PAPERORDRAW:
            if part2:
                return RESULTVALUE[RESULT_DRAW] + SHAPEVALUE[3]
            return RESULTVALUE[RESULT_LOSE] + SHAPEVALUE[2]
        else: # input == SCISSORSORWIN
            if part2:
                return RESULTVALUE[RESULT_WIN] + SHAPEVALUE[1]
            return RESULTVALUE[RESULT_DRAW] + SHAPEVALUE[3]


def puzzle(input, part2=False):
    result = 0

    for line in input:
        elf, second = line.split(" ")
        roundResult = RPS(elf, second, part2)
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
