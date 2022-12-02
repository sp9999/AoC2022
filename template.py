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
with open(".\input.txt", encoding="utf8") as fp:
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


def puzzle(input):
    result = 0
    return result


sp1 = puzzle(sample)
p1 = puzzle(lines)
# sp2 = puzzle(sample)
# p2 = puzzle(lines)

print("SP1: " + str(sp1))
print("SP2: " + str(sp2))
print("P1: " + str(p1))
print("P2: " + str(p2))

if p1 != 0 and submit(p1, part="a", day=DAY, year=YEAR) is None:
    submit(p2, part="b", day=DAY, year=YEAR)
