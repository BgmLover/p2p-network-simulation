import config
import utils

coverage_threshold = 0.95


def analyse():
    data = dict()
    for root_index in range(config.max_index):
        data[root_index] = dict()
        msg_id = 0
        for neighbor_size in config.neighbor_size_range:
            data[root_index][neighbor_size] = dict()
            for alpha in config.p_range:
                for msg_ttl in range(config.ttl_max):
                    file_name = str(root_index) + '_' + str(neighbor_size) + "_" + str(alpha) + "_" + \
                                str(msg_ttl) + "_" + str(msg_id) + ".json"
                    result = utils.load_result(config.save_dir + file_name)
                    msg_id = msg_id + 1
                    target_index = int(result['peer_size'] * coverage_threshold)
                    if result['coverage'] < target_index:
                        continue
                    if result['time_array'][target_index] > result['target_time']:
                        continue
                    data[root_index][neighbor_size][msg_id] = result

    best = dict()
    for root_index in range(config.max_index):
        best[root_index] = dict()
        for neighbor_size in config.neighbor_size_range:
            min_redundant = float('inf')
            min_case = None
            for case in data[root_index][neighbor_size]:
                if data[root_index][neighbor_size][case]['total_redundant'] < min_redundant:
                    min_redundant = data[root_index][neighbor_size][case]['total_redundant']
                    min_case = data[root_index][neighbor_size][case]
            best[root_index][neighbor_size] = min_case

    print("over")


if __name__ == '__main__':
    analyse()
