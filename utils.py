import config
import json
import os
import numpy as np


def save_result(time_array, total_redundant, network, msg, target_time, root_index):
    result = dict()
    result['neighbor_size'] = network.neighbor_size
    result['alpha'] = network.alpha
    result['total_redundant'] = total_redundant
    result['target_time'] = target_time
    result['coverage'] = len(np.where(time_array != float('inf'))[0])
    result['msg_ttl'] = msg.ttl
    result['msg_id'] = msg.id
    result['peer_size'] = network.peer_size
    result["time_array"] = list()
    for num in time_array:
        result["time_array"].append(float(num))

    f_dir = config.save_dir + str(root_index) + '/'
    if not os.path.exists(f_dir):
        os.makedirs(f_dir)
    file_name = str(network.neighbor_size) + "_" + str(network.alpha) + "_" + str(msg.ttl) + ".json"

    with open(f_dir + file_name, "w+") as f:
        json.dump(result, f)
        if config.show_log:
            print("save file " + config.save_dir + file_name)


def load_result(path):
    with open(path, 'r') as f:
        load_dict = json.load(f)
        return load_dict


def show_result():
    pass
