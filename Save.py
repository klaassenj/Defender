__author__ = 'Jason'

import os
import Fighter
import Weapons
path = 'res/saveData/data.txt'
def createFile():
    data = open(path, 'w')
    data.write(str(Fighter.player.level) + '\n')
    data.write(str(Fighter.player.xp) + '\n')
    data.write(str(Fighter.player.weapon.__class__.__name__) + '\n')
    data.close()
def readFile():
    if os.path.isfile(path):
        data = open(path,'r')
        lines = data.readlines()
        loadData = Data(lines)
        data.close()
        return loadData
    else:
        return None
class Data:
    def __init__(self, lines):
        self.lines = lines
        self.level = int(lines[0])
        self.xp = int(lines[1])
        self.weapon = lines[2]

