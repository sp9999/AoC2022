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

class Operation:
    def __init__(self, input):
        self.first, self.operand, self.second = input.split("= ")[1].split(" ")

    def doOperation(self, input):
        if self.operand == "+":
            if self.second == "old":
                return input + input
            else:
                return input + int(self.second)
        elif self.operand == "*":
            if self.second == "old":
                return input * input
            else:
                return input * int(self.second)
class Test:
    def __init__(self, divisible, true, false):
        self.divisible = divisible
        self.true = true
        self.false = false

class Monkey:
    def __init__(self, input):
        self.number = int(input[0].split(" ")[1][0])
        items = input[1].split(": ")[1].split(", ")
        self.items = []
        for i in items:
            self.items.append(int(i))
        self.operation = Operation(input[2])
        testDivisible = int(input[3].split("by ")[1])
        testTrue = int(input[4].split(" ")[-1])
        testFalse = int(input[5].split(" ")[-1])
        self.test = Test(testDivisible, testTrue, testFalse)
        self.inspections = 0

    def resolveMonkey(self, monkeys, part2, divisor):
        while len(self.items):
            self.inspections += 1
            currWorry = self.items.pop(0)
            newWorry = self.operation.doOperation(currWorry)
            if not part2:
                newWorry //= divisor
            else:
                newWorry = newWorry % divisor
            if newWorry % self.test.divisible == 0:
                monkeys[self.test.true].items.append(newWorry)
            else:
                monkeys[self.test.false].items.append(newWorry)

    def print(self):
        print(str(self.number) + ": " + str(self.inspections) + " | " + str(self.items))


def puzzle(input, part2=False):
    rounds = 20
    if part2:
        rounds = 10000
    monkeys = []
    for i in range(0, len(input), 7):
        monkeys.append(Monkey(input[i:i+6]))

    divisor = 1
    if part2:
        for m in monkeys:
            divisor *= m.test.divisible
    else:
        divisor = 3
    for i in range(0, rounds):
        for m in monkeys:
            m.resolveMonkey(monkeys, part2, divisor)

    inspections = []
    for m in monkeys:
        m.print()
        inspections.append(m.inspections)
    print("\n")

    inspections.sort()

    return inspections[-1] * inspections[-2]


sp1 = puzzle(sample)
p1 = puzzle(lines)
sp2 = puzzle(sample, True)
p2 = puzzle(lines, True)

print("SP1: " + str(sp1))   # 10605
print("SP2: " + str(sp2))   # 2713310158
print("P1: " + str(p1))     # 54036
print("P2: " + str(p2))     # 13237873355

if p1 != 0 and submit(p1, part="a", day=DAY, year=YEAR) is None:
    if p2 != 0:
        submit(p2, part="b", day=DAY, year=YEAR)