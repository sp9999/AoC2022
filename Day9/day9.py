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

DIR_ENUM = {
    "U": 0,
    "D": 1,
    "L": 2,
    "R": 3,
    "UL": 4,
    "UR": 5,
    "DL": 6,
    "DR": 7
}

DIR_DX_ENUM = {
    (0, 0): -1,
    (1, 0): 0,
    (-1, 0): 1,
    (0, -1): 2,
    (0, 1): 3,
    (1, -1): 4,
    (1, 1): 5,
    (-1, -1): 6,
    (-1, 1): 7

}

class Command:
    def __init__(self, line):
        direction, steps = line.split(" ")
        self.dir = DIR_ENUM[direction]
        self.steps = int(steps)



class Snake:
    def __init__(self):
        self.head = utility.Point()
        self.tail = utility.Point(-1, -1)
        self.uniquePositions = set()

    def move(self, index, dir, steps):
        for i in range(0, steps):
            dy = 0
            dx = 0
            if dir == 0:
                self.head.y += 1
                dy = 1
            elif dir == 1:
                self.head.y -= 1
                dy = -1
            elif dir == 2:
                self.head.x -= 1
                dx = -1
            else:
                self.head.x += 1
                dx = 1

            if dy != 0 and abs(self.head.y - self.tail.y) > 1:
                self.tail.y += dy
                self.tail.x = self.head.x
                self.uniquePositions.add((self.tail.y, self.tail.x))

            elif dx != 0 and abs(self.head.x - self.tail.x) > 1:
                self.tail.x += dx
                self.tail.y = self.head.y
                self.uniquePositions.add((self.tail.y, self.tail.x))

class Snake2:
    def __init__(self):
        self.body = []
        for i in range(0, -10, -1):
            self.body.append(utility.Point())
        self.uniquePositions = set((0,0))

    def move(self, index, dir, steps):

        if dir == -1 or index > 9:
            return

        for i in range(0, steps):
            if dir == 0:
                self.body[index].y += 1
            elif dir == 1:
                self.body[index].y -= 1
            elif dir == 2:
                self.body[index].x -= 1
            elif dir == 3:
                self.body[index].x += 1
            elif dir == 4:
                self.body[index].y += 1
                self.body[index].x -= 1
            elif dir == 5:
                self.body[index].y += 1
                self.body[index].x += 1
            elif dir == 6:
                self.body[index].y -= 1
                self.body[index].x -= 1
            elif dir == 7:
                self.body[index].y -= 1
                self.body[index].x += 1

            if index == 9:
                self.uniquePositions.add((self.body[index].y, self.body[index].x))
                return

            dy = 0
            dx = 0
            if abs(self.body[index].y - self.body[index + 1].y) > 1:
                dy = self.body[index].y - self.body[index + 1].y
                dy = int(dy/abs(dy))
                dx = self.body[index].x - self.body[index+1].x
                if abs(dx) > 1:
                    dx = int(dx/abs(dx))

            if abs(self.body[index].x - self.body[index + 1].x) > 1:
                dx = self.body[index].x - self.body[index + 1].x
                dx = int(dx/abs(dx))
                dy = self.body[index].y - self.body[index + 1].y
                if abs(dy) > 1:
                    dy = int(dy / abs(dy))

            self.move(index + 1, DIR_DX_ENUM[(dy, dx)], 1)


def playGame(input, part2=False):
    snake = Snake()
    if part2:
        snake = Snake2()
    for i in input:
        command = Command(i)
        snake.move(0, command.dir, command.steps)

    return snake.uniquePositions


def puzzle(input, part2=False):
    result = playGame(input, part2)
    return len(result)

sp1 = puzzle(sample)
p1 = puzzle(lines)
sp2 = puzzle(sample, True)
p2 = puzzle(lines, True)

print("SP1: " + str(sp1))   # 88
print("SP2: " + str(sp2))   # 36
print("P1: " + str(p1))     # 5858
print("P2: " + str(p2))     # 2602

if p1 != 0 and submit(p1, part="a", day=DAY, year=YEAR) is None:
    if p2 != 0:
        submit(p2, part="b", day=DAY, year=YEAR)