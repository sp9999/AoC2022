def inputDataToLines(input):
    return input.split('\n')

def listStringToListNum(input):
    return [eval(i) for i in input]

def inputDataToInt2DArray(input):
    array2D = []
    for i in input:
        row = []
        for c in i:
            row.append(int(c))
        array2D.append(row)
    return array2D


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def getDistSquared(self, p2):
        dx = abs(self.x - p2.x)
        dy = abs(self.y - p2.y)
        return dx * dx + dy * dy

