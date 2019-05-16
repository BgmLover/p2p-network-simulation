import os
import config

if __name__ == '__main__':
    process_size = int(config.max_index / 100)
    for index in range(process_size):
        command = "python3 simulate_one.py " + str(index) + " &"
        os.system(command)
        # print(str(index) + "processes start")
