import sys
import config
from p2p_network_time import Network, simulate_msgs


def simulate_one(index):
    s_config = config.Config()
    network = Network(s_config.relay_possibility, s_config.peer_size, s_config.neighbor_size)
    network.generate_nodes()
    simulate_msgs(network, index)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        for i in range(10):
            simulate_one(int(10 * sys.argv[1] + i))
    else:
        print("wrong parameters")
