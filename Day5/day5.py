import utility
import session
import os
import sys
from aocd.models import Puzzle
from aocd import submit
import queue
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
        sample.append(line)

## CONVERT INPUT STRING LIST TO NUMBERS IF POSSIBLE
try:
    nums = utility.listStringToListNum(lines)
    sampleNum = utility.listStringToListNum(sample)
except:
    nums = []
    sampleNum = []

sp1 = sp2 = p1 = p2 = 0

class Stacks:
    def __init__(self, input):
        self.lineWithStackNumbers = 0
        self.stackCount = 0
        self.s = []
        it = 0
        for i in input:
            if i[1] == '1':
                self.lineWithStackNumbers = it
                self.stackCount = int(i.strip().split(' ')[-1])
                break
            it += 1

        for i in range(0, self.stackCount):
            self.s.append([])
        for i in range(self.lineWithStackNumbers - 1, -1, -1):
            for x in range(0, len(input[self.lineWithStackNumbers])):
                stackNum = input[self.lineWithStackNumbers][x]
                if not (stackNum == ' ' or stackNum == '\n') and len(input[i]) > x and not (input[i][x] == ' ' or input[i][x] == '\n'):
                    self.s[int(stackNum)-1].append(input[i][x])

    def toString(self):
        for i in range(0, self.stackCount):
            print(str(i + 1) + ": " + str(self.s[i]))
        print("\n")

    def move(self, count, src, dst, part2):
        part2Temp = []
        for i in range(0, count):
            if not part2:
                self.s[dst].append(self.s[src].pop())
            else:
                part2Temp.append(self.s[src].pop())

        for i in range(0, len(part2Temp)):
            self.s[dst].append(part2Temp.pop())


    def topCrates(self):
        str = ""
        for i in range(0, len(self.s)):
            str += self.s[i][-1]
        return str

def parseAction(input):
    a, count, b, src, c, dst = input.split(' ')
    return int(count), int(src) - 1, int(dst) - 1

def puzzle(input, part2=False):
    stacks = Stacks(input)

    actionStart = stacks.lineWithStackNumbers + 2
    for i in range(actionStart, len(input)):
        count, src, dst = parseAction(input[i])
        stacks.move(count, src, dst, part2)

    stacks.toString()
    return stacks.topCrates()

sp1 = puzzle(sample)
p1 = puzzle(lines)
sp2 = puzzle(sample, True)
p2 = puzzle(lines, True)

print("SP1: " + str(sp1))
print("SP2: " + str(sp2))
print("P1: " + str(p1))
print("P2: " + str(p2))

if p1 != 0 and submit(p1, part="a", day=DAY, year=YEAR) is None:
    if p2 != 0:
        submit(p2, part="b", day=DAY, year=YEAR)