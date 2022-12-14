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

class Signal:
    def __init__(self, obj):
        self.s = obj

    def __lt__(self, other):
        return isPairInRightOrder(self.s, other.s) == -1

def isPairInRightOrder(p0, p1):
    i = 0
    while i < len(p0) and i < len(p1):
        p0Val = p0[i]
        p1Val = p1[i]
        checkNestedPair = 0
        # both values are integer
        if isinstance(p0Val, int) and isinstance(p1Val, int):
            if p0Val < p1Val:
                return -1
            elif p0Val > p1Val:
                return 1
        # both lists
        elif isinstance(p0Val, list) and isinstance(p1Val, list):
            checkNestedPair = isPairInRightOrder(p0Val, p1Val)
        # one list one int
        elif isinstance(p0Val, int) and isinstance(p1Val, list):
            checkNestedPair = isPairInRightOrder([p0Val], p1[i])
        else:
            checkNestedPair = isPairInRightOrder(p0[i], [p1Val])

        if checkNestedPair != 0:
            return checkNestedPair
        i += 1

    if i == len(p0) and i < len(p1):
        return -1
    elif i < len(p0) and i == len(p1):
        return 1
    else:
        return 0


def getRightOrderPairsSum(pairs):
    result = 0
    i = 1
    for p in pairs:
        if isPairInRightOrder(p[0], p[1]) == -1:
            result += i
        i += 1
    return result


def parseInput(line, start = 1):
    list = []
    val = ""
    i = start
    while i < len(line):
        if line[i] == "[":
            item, newI = parseInput(line, i + 1)
            list.append(item)
            i = newI
        elif line[i] == "]":
            if len(val) > 0:
                list.append(int(val))
            return list, i
        elif line[i] == ",":
            if len(val) > 0:
                list.append(int(val))
            val = ""
        else:
            val += line[i]
        i += 1
    return list, -1

from functools import cmp_to_key
def puzzle(input, part2=False):
    pairs = []
    all = []
    for i in range(0, len(input), 3):
        l1 = eval(input[i])
        l2 = eval(input[i+1])
        pairs.append((l1, l2))

        #all.append(l1)
        #all.append(l2)
        all.append(Signal(l1))
        all.append(Signal(l2))
    if not part2:
        result = getRightOrderPairsSum(pairs)
    else:
        decoder2 = eval("[[2]]")
        decoder6 = eval("[[6]]")
        #all.append(decoder2)
        #all.append(decoder6)
        all.append(Signal(decoder2))
        all.append(Signal(decoder6))
        sortedList = sorted(all)
        result = 0
        for i in range(0, len(sortedList)):
            if sortedList[i] == decoder2:
                result = (i + 1)
            elif sortedList[i] == decoder6:
                result *= (i + 1)
                break
    return result

sp1 = puzzle(sample)
p1 = puzzle(lines)
sp2 = puzzle(sample, True)
p2 = puzzle(lines, True)

print("SP1: " + str(sp1))   # 13
print("SP2: " + str(sp2))   # 140
print("P1: " + str(p1))     # 6568
print("P2: " + str(p2))     # 19493

if p1 != 0 and submit(p1, part="a", day=DAY, year=YEAR) is None:
    if p2 != 0:
        submit(p2, part="b", day=DAY, year=YEAR)