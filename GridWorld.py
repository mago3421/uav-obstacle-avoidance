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

    def gridDefine(self):
        environment = [['-' for x in range(self.w)] for y in range(self.h)]
        environment[self.goal_row][self.goal_col] = '!'
        environment[self.agent_row][self.agent_col] = 'O'
        length = len(self.static_obstacles)
        for x in range(0,length,2):
              environment[x][x+1]='*'

        # print(self.w, self.h, self.goal_row, self.goal_col,self.agent_row,self.agent_col,self.stat_no,self.static_obstacles_row, self.static_obstacles_col)
        # print(self.static_obstacles)
        for i in range(0,self.h):
            for j in range(0,self.w):
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
    print (text_in_file)

    grid = GridWorld(text_in_file)
    grid.gridDefine()
