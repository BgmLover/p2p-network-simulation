import os
import config

if __name__ == '__main__':
    for index in config.max_index:
        command = "python3 simulate_one.py " + str(index)
        os.system(command)
