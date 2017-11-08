class GridWorld:
    def __init__(self, text):
        self.w = int(self.find_between(text,"SIZE","SA"))
        self.h = int(self.find_between(text, "SA", "."))
        self.goal_row = int(self.find_between(text,"GOAL","GA"))
        self.goal_col = int(self.find_between(text,"GA","."))
        self.agent_row = int(self.find_between(text, "AGENT", "AA"))
        self.agent_col = int(self.find_between(text, "AA", "."))
        self.stat_no = int(self.find_between(text, "STANO", "."))
        self.static_obstacles = []

        for self.x in range(1,(self.stat_no+1)):
            self.static = "STATIC"
            self.sta = "STA"
            self.static+=str(self.x)
            self.sta+=str(self.x)
            self.static_obstacles_row = int(self.find_between(text, self.static, self.sta))
            self.static_obstacles_col = int(self.find_between(text, self.sta, "."))
            # print ("x ->",self.x)
            # print(self.static)
            # print(self.sta)
            self.static_obstacles.append(self.static_obstacles_row)
            self.static_obstacles.append(self.static_obstacles_col)

    def surroundOuterGrid(self, rowEnd, colEnd, environment):
        rowStart = 1
        colStart = 1
        for col in range(colStart-1,colEnd+1):
            environment[rowStart-1][col] = '#'
            environment[rowEnd+1][col] = '#'


        for row in range(rowStart - 1, rowEnd+2):
            environment[row][colStart-1] = '#'
            environment[row][colEnd+1] = '#'

        return environment

    def surroundInnerGrid(self, rowEnd, colEnd, environment):
        rowStart = 1
        colStart = 1
        for col in range(colStart,colEnd):
            if environment[rowStart][col] == '-':
                environment[rowStart][col] = 'x'
            if environment[rowEnd][col] == '-':
                environment[rowEnd][col] = 'x'

        for row in range(rowStart, rowEnd+1):
            if environment[row][colStart] == '-':
                environment[row][colStart] = 'x'
            if environment[row][colEnd] == '-':
                environment[row][colEnd] = 'x'

        return environment

    def surroundObstacleGrid(self, rowStart, colStart, environment):
        rowEnd = rowStart + 1
        colEnd = colStart + 1
        rowStart = rowStart - 1
        colStart = colStart - 1
        for col in range(colStart, colEnd):
            if environment[rowStart][col] == '-':
                environment[rowStart][col] = 'x'
            if environment[rowEnd][col] == '-':
                environment[rowEnd][col] = 'x'

        for row in range(rowStart, rowEnd+1):
            if environment[row][colStart] == '-':
                environment[row][colStart] = 'x'
            if environment[row][colEnd] == '-':
                environment[row][colEnd] = 'x'

        return environment

    def surroundGoalGrid(self, rowStart, colStart, environment):
        rowEnd = rowStart + 1
        colEnd = colStart + 1
        rowStart = rowStart - 1
        colStart = colStart - 1
        for col in range(colStart, colEnd):
            if environment[rowStart][col] == '-':
                environment[rowStart][col] = '^'
            if environment[rowEnd][col] == '-':
                environment[rowEnd][col] = '^'

        for row in range(rowStart, rowEnd+1):
            if environment[row][colStart] == '-':
                environment[row][colStart] = '^'
            if environment[row][colEnd] == '-':
                environment[row][colEnd] = '^'

        return environment

    def gridDefine(self):
        environment = [['-' for x in range(0,self.w+2)] for y in range(0,self.h+2)]
        environment = self.surroundOuterGrid( self.h,self.w,environment)
        environment[self.goal_row][self.goal_col]='!'
        environment = self.surroundGoalGrid(self.goal_row, self.goal_col, environment)
        environment[self.agent_row][self.agent_col] = 'O'
        length = len(self.static_obstacles)
        for x in range(0, length, 2):
            environment[self.static_obstacles[x]][self.static_obstacles[x+1]] = '*'
            environment = self.surroundObstacleGrid(self.static_obstacles[x], self.static_obstacles[x+1], environment)

        environment = self.surroundInnerGrid(self.h, self.w, environment)
        # print(self.w, self.h, self.goal_row, self.goal_col,self.agent_row,self.agent_col,self.stat_no,self.static_obstacles_row, self.static_obstacles_col)
        # print(self.static_obstacles)
        for i in range(0,self.h+2):
            for j in range(0,self.w+2):
                print(environment[i][j],end='')
            print()
        return environment

    def find_between(self, s, first, last):
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""

if __name__ == "__main__":
    env_file = open("Environment.txt", "r")
    text_in_file = env_file.readline()
    # print (text_in_file)

    grid = GridWorld(text_in_file)
    grid.gridDefine()
