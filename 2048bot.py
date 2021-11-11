import random
import copy

class UndefinedDirectionError(Exception):
    def __init__(self):
        super().__init__('UndefinedDirectionError')

class FinishedGameError(Exception):
    def __init__(self):
        super().__init__('The game has already over.')

class Class2048:
    sq = [[0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]]
    score = 0
    over = False

    def __init__(self):
        self.__randomSpawn()
        self.__randomSpawn()

    def __isGameOver(self):
        cnt = 0
        sw = [0, 1, -1]
        ne = [0, 1, -1]

        for i in range(0, 4):
            for j in range(0, 4):
                tmp_cnt, tmp_chk = 0, 0
                for x in range(0, 3):
                    for y in range(0, 3):
                        if(sw[x]+i > -1 and sw[x]+i < 4 and ne[y]+j > -1 and ne[y]+j < 4 and (abs(sw[x]) + abs(ne[y]) == 1)):
                            tmp_cnt += 1
                            if(self.sq[sw[x]+i][ne[y]+j] != self.sq[i][j] and self.sq[sw[x]+i][ne[y]+j] != 0):
                                tmp_chk += 1
                if(tmp_chk == tmp_cnt):
                    cnt += 1
        if(cnt == 16):
            return True
        return False

    def __randomSpawn(self):
        while True:
            a, b = random.randrange(0, 4), random.randrange(0, 4)
            spawn = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
            if(self.sq[a][b] == 0):
                self.sq[a][b] = random.choice(spawn)
                break

    def __subMergeUp(self):
        for i in range(0, 4):
            line = []
            for j in range(0, 4): line.append(self.sq[j][i]) 
            cnt = 0
            for x in range(0, 4):
                if(line[x] != 0):
                    line[cnt] = line[x]
                    if(cnt != x):
                        line[x] = 0
                    cnt += 1
            for x in range(0, 3):
                if(line[x] == line[x+1]):
                    line[x], line[x+1] = line[x]+line[x+1], 0
                    self.score += line[x]
            cnt = 0
            for x in range(0, 4):
                if(line[x] != 0):
                    line[cnt] = line[x]
                    if(cnt != x):
                        line[x] = 0
                    cnt += 1
            for j in range(0, 4): self.sq[j][i] = line[j]
    def __subMergeDown(self):
        for i in range(0, 4):
            line = []
            for j in range(0, 4): line.append(self.sq[j][i])
            cnt = 3
            for x in range(3, -1, -1):
                if(line[x] != 0):
                    line[cnt] = line[x]
                    if(cnt != x):
                        line[x] = 0
                    cnt -= 1
            for x in range(3, 0, -1):
                if(line[x] == line[x-1]):
                    line[x], line[x-1] = line[x]+line[x-1], 0
                    self.score += line[x]
            cnt = 3
            for x in range(3, -1, -1):
                if(line[x] != 0):
                    line[cnt] = line[x]
                    if(cnt != x):
                        line[x] = 0
                    cnt -= 1
            for j in range(0, 4): self.sq[j][i] = line[j]
    def __subMergeLeft(self):
        for i in range(0, 4):
            line = self.sq[i]
            cnt = 0
            for x in range(0, 4):
                if(line[x] != 0):
                    line[cnt] = line[x]
                    if(cnt != x):
                        line[x] = 0
                    cnt += 1
            for x in range(0, 3):
                if(line[x] == line[x+1]):
                    line[x], line[x+1] = line[x]+line[x+1], 0
                    self.score += line[x]
            cnt = 0
            for x in range(0, 4):
                if(line[x] != 0):
                    line[cnt] = line[x]
                    if(cnt != x):
                        line[x] = 0
                    cnt += 1
            self.sq[i] = line
    def __subMergeRight(self):
        for i in range(0, 4):
            line = self.sq[i]
            cnt = 3
            for x in range(3, -1, -1):
                if(line[x] != 0):
                    line[cnt] = line[x]
                    if(cnt != x):
                        line[x] = 0
                    cnt -= 1
            for x in range(3, 0, -1):
                if(line[x] == line[x-1]):
                    line[x], line[x-1] = line[x]+line[x-1], 0
                    self.score += line[x]
            cnt = 3
            for x in range(3, -1, -1):
                if(line[x] != 0):
                    line[cnt] = line[x]
                    if(cnt != x):
                        line[x] = 0
                    cnt -= 1
            self.sq[i] = line

    def merge(self, direction): # 정상적으로 턴 넘기기에 성공하면 0, 게임이 끝났다면 -1
        if(self.over):
            raise FinishedGameError
        if(direction == 'up'):
            prv = copy.deepcopy(self.sq)
            self.__subMergeUp()
            if(not prv == self.sq):
                self.__randomSpawn()
        elif(direction == 'down'):
            prv = copy.deepcopy(self.sq)
            self.__subMergeDown()
            if(not prv == self.sq):
                self.__randomSpawn()
        elif(direction == 'left'):
            prv = copy.deepcopy(self.sq)
            self.__subMergeLeft()
            if(not prv == self.sq):
                self.__randomSpawn()
        elif(direction == 'right'):
            prv = copy.deepcopy(self.sq)
            self.__subMergeRight()
            if(not prv == self.sq):
                self.__randomSpawn()
        else:
            raise UndefinedDirectionError

        if(self.__isGameOver()):
            over = True
            return -1
        
        return 0