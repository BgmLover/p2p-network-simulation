from p2p_network_time import Node
import matplotlib.pyplot as plt
import numpy as np
import config
import utils


def analyse():
    index_max = config.max_index
    data = dict()
    for root_index in range(index_max):
        data[root_index] = dict()
        msg_id = 0
        for neighbor_size in config.neighbor_size_range:
            data[root_index][neighbor_size] = dict()
            for alpha in config.p_range:
                for msg_ttl in range(config.ttl_max):
                    f_dir = config.save_dir + str(root_index) + '/'
                    file_name = str(neighbor_size) + "_" + str(alpha) + "_" + str(msg_ttl) + ".json"

                    result = utils.load_result(f_dir + file_name)
                    msg_id = msg_id + 1
                    target_index = int(result['peer_size'] * config.target_coverage)
                    if result['coverage'] < target_index:
                        continue
                    if result['time_array'][target_index] > result['target_time']:
                        continue
                    if result['time_array'][target_index] > config.target_time:
                        continue
                    data[root_index][neighbor_size][msg_id] = result

    good = dict()
    for root_index in range(index_max):
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
    for root_index in range(index_max):
        min_redundant = float('inf')
        for neighbor_size in good[root_index]:
            if good[root_index][neighbor_size] is not None and good[root_index][neighbor_size]['total_redundant'] < min_redundant:
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


def plot_coverage_time():
    file_names = [
        "8_0.3_4.json",
        "9_0.1_2.json",
        "5_0.4_3.json",
        "10_0.2_1.json",
        "13_0.1_0.json"
    ]
    plt.rcParams['savefig.dpi'] = 500
    plt.rcParams['figure.dpi'] = 500
    for file_name in file_names:
        f_dir = config.save_dir + str(0)+'/'
        result = utils.load_result(f_dir + file_name)
        time_array = np.array(result['time_array'])

        t_end = time_array[len(time_array) - 1]
        for end in reversed(time_array):
            if end != Node.max_transfer_time:
                t_end = end
                break
        t = np.arange(0, t_end, 0.01)
        result = []
        last_value = 0
        for value in t:
            indexes = np.where(time_array > value)
            if len(indexes) > 0 and len(indexes[0]) > 0:
                result.append((1 + indexes[0][0]) / len(time_array) * 100)
                last_value = result[len(result) - 1]
            else:
                result.append(last_value)
        file_name_split = file_name.split('_')
        neighbor_size = file_name_split[0]
        p = file_name_split[1]
        ttl = file_name_split[2]
        label = "neighbor_size=" + neighbor_size + ", p=" + p + ", ttl=" + ttl
        plt.plot(t, result, label=label)

    plt.xlabel("message propagation time (s)")
    plt.ylabel("message coverage (%)")
    plt.title("Coverage v.s Time")
    plt.legend(loc='best', prop={'size': 6})
    plt.show()


def plot_coverage_ttl_neighborsize():
    plt.rcParams['savefig.dpi'] = 500
    plt.rcParams['figure.dpi'] = 500
    f_dir = config.save_dir + str(0) + '/'
    for neighbor_size in config.neighbor_size_range:
        coverage = []
        for ttl in range(7):
            msg_id = (neighbor_size - 5) * 110 + ttl
            file_name = str(neighbor_size) + "_0_" + str(ttl) + '.json'
            result = utils.load_result(f_dir + file_name)
            coverage.append(result['coverage'] / 10)
        plt.plot(list(range(7)), coverage, label="neighbor_size = " + str(neighbor_size))

    plt.xlabel("message ttl")
    plt.ylabel("message coverage (%)")
    plt.title("Coverage v.s TTL (p=0)")
    plt.legend(loc='best', prop={'size': 6})
    plt.show()


def plot_coverage_p_ttl():
    plt.rcParams['savefig.dpi'] = 500
    plt.rcParams['figure.dpi'] = 500
    f_dir = config.save_dir + str(8) + '/'
    for ttl in range(5):
        coverage = []
        for p in config.p_range:
            file_name = "5_" + str(p) + "_" + str(ttl)  + '.json'
            result = utils.load_result(f_dir + file_name)
            coverage.append(result['coverage'] / 10)
        plt.plot(config.p_range, coverage, label="ttl = " + str(ttl))

    plt.xlabel("message relay probability")
    plt.ylabel("message coverage (%)")
    plt.title("Coverage v.s Relay Probability (neighbor_size = 5)")
    plt.legend(loc='best', prop={'size': 6})
    plt.show()


def plot_coverage_p_ttl_under_targettime():
    plt.rcParams['savefig.dpi'] = 500
    plt.rcParams['figure.dpi'] = 500
    f_dir = config.save_dir + str(8) + '/'
    for ttl in range(5):
        coverage = []
        for p in config.p_range:
            file_name = "5_" + str(p) + "_" + str(ttl)  + '.json'
            result = utils.load_result(f_dir + file_name)
            time_array = np.array(result['time_array'])
            indexes = np.where(time_array >= result['target_time'])
            coverage.append(((1 + indexes[0][0]) / len(time_array) * 100))
        plt.plot(config.p_range, coverage, label="ttl = " + str(ttl))

    plt.xlabel("message relay probability")
    plt.ylabel("message coverage (%)")
    plt.title("Coverage v.s Relay Probability at Target_time (neighbor_size = 5)")
    plt.legend(loc='best', prop={'size': 6})
    plt.show()


def plot_redundancy_p_ttl():
    plt.rcParams['savefig.dpi'] = 500
    plt.rcParams['figure.dpi'] = 500
    f_dir = config.save_dir + str(0) + '/'
    for ttl in range(7):
        redundancy = []
        for p in config.p_range:
            file_name = "7_" + str(p) + "_" + str(ttl)  + '.json'
            result = utils.load_result(f_dir + file_name)
            redundancy.append(result['total_redundant'])
        plt.plot(config.p_range, redundancy, label="ttl = " + str(ttl))

    plt.xlabel("message relay probability")
    plt.ylabel("message redundancy ")
    plt.title("Redundancy v.s Relay Probability (neighbor_size = 7)")
    plt.legend(loc='best', prop={'size': 6})
    plt.show()


def plot_redundancy_neighborsize_ttl():
    plt.rcParams['savefig.dpi'] = 500
    plt.rcParams['figure.dpi'] = 500

    for ttl in range(6):
        redundancy = []
        for neighbor_size in config.neighbor_size_range:
            total_result = 0
            for index in range(config.max_index):
                msg_id = (neighbor_size - 5) * 110 + ttl
                file_name = str(neighbor_size) + "_0_" + str(ttl)  + '.json'
                f_dir = config.save_dir + str(index) + '/'
                result = utils.load_result(f_dir + file_name)
                total_result = total_result + result['total_redundant']
            redundancy.append(total_result / len(range(config.max_index)))
        plt.plot(config.neighbor_size_range, redundancy, label="ttl = " + str(ttl))

    plt.xlabel("network neighbor size")
    plt.ylabel("message redundancy ")
    plt.title("Redundancy v.s Neighbor_size (p = 0)")
    plt.legend(loc='best', prop={'size': 6})
    plt.show()


def plot_targettime_neighborsize():
    plt.rcParams['savefig.dpi'] = 500
    plt.rcParams['figure.dpi'] = 500
    f_dir = config.save_dir + str(0) + '/'
    target_time = []
    for neighbor_size in config.neighbor_size_range:
        file_name = str(neighbor_size) + "_0_" + str(0)  + '.json'
        result = utils.load_result(f_dir + file_name)
        target_time.append(result['target_time'])
    plt.plot(config.neighbor_size_range, target_time)

    plt.xlabel("network neighbor size")
    plt.ylabel("message target_time (s)")
    plt.title("Target_time v.s Neighbor_size ")
    plt.legend(loc='best', prop={'size': 6})
    plt.show()


if __name__ == '__main__':
    analyse()
    # plot_coverage_time()
    # plot_coverage_ttl_neighborsize()
    # plot_coverage_p_ttl()
    # plot_coverage_p_ttl_under_targettime()
    # plot_redundancy_p_ttl()
    # plot_redundancy_neighborsize_ttl()
    # plot_targettime_neighborsize()
