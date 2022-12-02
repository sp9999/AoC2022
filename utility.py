def inputDataToLines(input):
    return input.split('\n')

def listStringToListNum(input):
    return [eval(i) for i in input]




class Command:
    def __init__(self, line):
        command, numberString = line.split(' ')

        self.command = command
        self.number = int(numberString[1:])
        self.positive = numberString[:1] == '+'
