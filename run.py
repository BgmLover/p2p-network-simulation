import os
import config

if __name__ == '__main__':
    for index in range(config.process_size):
        command = "python3 simulate_one.py " + str(index) + " &"
        os.system(command)
        # print(str(index) + "processes start")
