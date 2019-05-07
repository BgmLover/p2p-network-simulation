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

    if not os.path.exists(config.save_dir):
        os.makedirs(config.save_dir)
    file_name = str(root_index) + '_' + str(network.neighbor_size) + "_" + str(network.alpha) + "_" + str(
        msg.ttl) + "_" + str(msg.id) + ".json"

    with open(config.save_dir + file_name, "w+") as f:
        json.dump(result, f)
        print("save file " + config.save_dir + file_name)


def load_result(path):
    with open(path, 'r') as f:
        load_dict = json.load(f)
        return load_dict


def show_result():
    pass
