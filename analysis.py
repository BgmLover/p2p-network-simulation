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

    good = dict()
    for root_index in range(config.max_index):
        good[root_index] = dict()
        for neighbor_size in config.neighbor_size_range:
            min_redundant = float('inf')
            min_case = None
            for case in data[root_index][neighbor_size]:
                if data[root_index][neighbor_size][case]['total_redundant'] < min_redundant:
                    min_redundant = data[root_index][neighbor_size][case]['total_redundant']
                    min_case = data[root_index][neighbor_size][case]
            good[root_index][neighbor_size] = min_case

    best = dict()
    for root_index in range(config.max_index):
        min_redundant = float('inf')
        for neighbor_size in good[root_index]:
            if good[root_index][neighbor_size]['target_time'] < config.target_time \
                    and good[root_index][neighbor_size]['total_redundant'] < min_redundant:
                min_redundant = good[root_index][neighbor_size]['total_redundant']
                best[root_index] = good[root_index][neighbor_size]

    best_neighbor_size = dict()
    best_ttl = dict()
    best_p = dict()
    best_set = dict()
    for index in best:
        if best_neighbor_size.get(best[index]['neighbor_size']) is None:
            best_neighbor_size[best[index]['neighbor_size']] = 1
        else:
            best_neighbor_size[best[index]['neighbor_size']] = best_neighbor_size[best[index]['neighbor_size']] + 1

        if best_ttl.get(best[index]['msg_ttl']) is None:
            best_ttl[best[index]['msg_ttl']] = 1
        else:
            best_ttl[best[index]['msg_ttl']] = best_ttl[best[index]['msg_ttl']] + 1

        if best_p.get(best[index]['alpha']) is None:
            best_p[best[index]['alpha']] = 1
        else:
            best_p[best[index]['alpha']] = best_p[best[index]['alpha']] + 1

        set_value = best[index]['neighbor_size'] * 1000 + best[index]['msg_ttl'] * 100 + best[index]['alpha'] * 10
        if best_set.get(set_value) is None:
            best_set[set_value] = 1
        else:
            best_set[set_value] = best_set[set_value] + 1

    print(best_neighbor_size)
    print(best_ttl)
    print(best_p)
    print(best_set)

    print("over")


if __name__ == '__main__':
    analyse()
