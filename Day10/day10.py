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

class CRT:
    def __init__(self):
        self.grid = []
        for y in range(0, 6):
            row = []
            for x in range(0, 40):
                row.append('.')
            self.grid.append(row)

    def print(self):
        for y in range(0, 6):
            print(self.grid[y])
        print("\n")

    def light(self, y, x):
        self.grid[y][x] = '#'

def puzzle(input, part2=False):
    i = 0
    x = 1
    queueAdd = []

    if not part2:
        signalStrengths = []
        signalTestCycle = 20
        for cycleCount in range(1, 221):
            if cycleCount == signalTestCycle:
                signalStrengths.append(cycleCount * x)
                signalTestCycle += 40

            if len(queueAdd) > 0:
                x += queueAdd.pop(0)
            else:
                if input[i] != "noop":
                    queueAdd.append(int(input[i].split(" ")[1]))
                i += 1

        return sum(signalStrengths)
    else:
        crt = CRT()
        for cycleCount in range(0, 240):
            if x - 1 <= cycleCount % 40 <= x + 1:
                crt.light(int(cycleCount / 40), cycleCount % 40)
            if len(queueAdd) > 0:
                x += queueAdd.pop(0)
            else:
                if input[i] != "noop":
                    queueAdd.append(int(input[i].split(" ")[1]))
                i += 1

        crt.print()
    return 0

sp1 = puzzle(sample)
p1 = puzzle(lines)
sp2 = puzzle(sample, True)
p2 = puzzle(lines, True)

print("SP1: " + str(sp1))   # 13140
print("SP2: " + str(sp2))   # gibberish
print("P1: " + str(p1))     # 17380
print("P2: " + str(p2))     # FGCUZREC

if p1 != 0 and submit(p1, part="a", day=DAY, year=YEAR) is None:
    if p2 != 0:
        submit(p2, part="b", day=DAY, year=YEAR)