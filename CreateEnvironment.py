class CreateEnvironment:
    def __init__(self):
        test = 0

    def create(self, file, size_row, size_col, agent_row, agent_col, goal_row, goal_col, static_number, static_list):
        text='SIZE'+size_row+'SA'+size_col+'.GOAL'+goal_row+'GA'+goal_col+'.AGENT'+agent_row+'AA'+agent_col+'.STANO'+static_number+'.'
        count = 0
        countInc = 1
        for i in range(0,int(static_number)):
            text+='STATIC'+str(countInc)+str(static_list[count])
            count+=1
            text+='STA'+str(countInc)+str(static_list[count])+'.'
            countInc+=1
            count+=1
        text+='\n'
        print(text)
        file.write(text)




if __name__ == "__main__":
    env_file = open("Environment.txt", "w")
    obj = CreateEnvironment()

    obj.create(env_file, size_row='10', size_col='10', agent_row='1', agent_col='1', goal_row='10', goal_col='10', static_number='2', static_list=[1,3,2,4])

