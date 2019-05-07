import copy
import numpy as np
import matplotlib.pyplot as plt
import threading
import config
import queue
import graph
import utils


class Message:
    def __init__(self, msg_id, ttl):
        self.id = msg_id
        self.ttl = ttl


class Node:
    def __init__(self, point, alpha, node_id):
        self.node_id = node_id
        self.coordinate = point
        self.neighbors = dict()
        self.received_msg = dict()
        self.relaying_msg = dict()
        self.relayed_msg = []
        self.alpha = alpha

    def receive_msg(self, msg, msg_from):
        if msg.id not in self.received_msg:
            self.received_msg[msg.id] = dict()
            self.received_msg[msg.id][msg_from] = msg.ttl
            self.relaying_msg[msg.id] = dict()
            self.relaying_msg[msg.id][msg_from] = msg
        else:
            self.received_msg[msg.id][msg_from] = msg.ttl
            if msg.id not in self.relayed_msg:
                if self.relaying_msg.get(msg.id) is None:
                    self.relaying_msg[msg.id] = dict()
                self.relaying_msg[msg.id][msg_from] = msg

    def relay_msg(self, sent_by):
        try:
            while self.relaying_msg.__len__() > 0:
                temp = self.relaying_msg.popitem()
                msg = temp[1][sent_by]
                relay_msg = copy.deepcopy(msg)
                relay_msg.ttl = relay_msg.ttl - 1
                self.relayed_msg.append(msg.id)
                for neighbor in self.neighbors:
                    if neighbor == sent_by:
                        continue
                    if msg.ttl > 0:
                        neighbor.receive_msg(relay_msg, self)
                    else:
                        t = np.random.rand()
                        if t < self.alpha:
                            neighbor.receive_msg(relay_msg, self)
                        else:
                            # print(t)
                            self.neighbors[neighbor] = graph.max_distance
        except Exception as e:
            print(e)

    def broadcast_msg(self, msg):
        self.received_msg[msg.id] = dict()
        for neighbor in self.neighbors:
            neighbor.receive_msg(msg, self)

    def add_neighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors[neighbor] = self.get_distance_of_neighbor(neighbor)

    def reset_distance(self):
        for neighbor in self.neighbors:
            self.neighbors[neighbor] = self.get_distance_of_neighbor(neighbor)

    def get_distance_of_neighbor(self, neighbor):
        return self.coordinate.get_distance_of_point(neighbor.coordinate)

    def __str__(self):
        return "node_" + str(self.node_id)

    def __eq__(self, other):
        return isinstance(other, Node) and self.node_id == other.node_id

    def __hash__(self):
        return self.node_id


class Network:
    def __init__(self, alpha, peer_size, neighbor_size):
        self.nodes = []
        self.alpha = alpha
        self.peer_size = peer_size
        self.neighbor_size = neighbor_size

    def check_is_connected_graph(self):
        if self.nodes.__len__() < 1:
            return True
        root_node = self.nodes[0]
        q = queue.Queue()
        connected_nodes = dict()
        q.put(root_node)
        connected_nodes[0] = True
        while not q.empty():
            node = q.get()
            for neighbor in node.neighbors:
                if neighbor.node_id not in connected_nodes:
                    connected_nodes[neighbor.node_id] = True
                    q.put(neighbor)
        return connected_nodes.__len__() == self.nodes.__len__()

    def generate_nodes(self, xbegin, xend, ybegin, yend):
        points = graph.random_generate_point(xbegin, xend, ybegin, yend, self.peer_size)
        index = 0
        for point in points:
            self.nodes.append(Node(point, self.alpha, index))
            index = index + 1

    def update_alpha(self, alpha):
        self.alpha = alpha
        for node in self.nodes:
            node.alpha = alpha

    def copy(self):
        new_network = Network(self.alpha, self.peer_size, self.neighbor_size)
        for node in self.nodes:
            new_network.nodes.append(Node(graph.Point(node.coordinate.x, node.coordinate.y), self.alpha, node.node_id))

        for i in range(len(self.nodes)):
            for neighbor in self.nodes[i].neighbors:
                new_network.nodes[i].neighbors[new_network.nodes[neighbor.node_id]] = self.nodes[i].neighbors[neighbor]

        return new_network

    def assign_neighbors(self):
        for node in self.nodes:
            indexes = np.random.randint(0, self.nodes.__len__(), self.neighbor_size * 2)
            for index in indexes:
                if index == node.node_id:
                    continue
                c_node = self.nodes[index]
                if node.neighbors.__len__() < self.neighbor_size and c_node.neighbors.__len__() < self.neighbor_size:
                    node.add_neighbor(self.nodes[index])
                    c_node.add_neighbor(node)
                if node.neighbors.__len__() == self.neighbor_size:
                    break

    def clear_neighbors(self):
        for node in self.nodes:
            node.neighbors.clear()

    def reset_distance(self):
        for node in self.nodes:
            node.reset_distance()

    def show_neighbors(self):
        plt.figure(1)
        node_pair = dict()
        for node in self.nodes:
            if node_pair.get(node.node_id) is None:
                node_pair[node.node_id] = []
            for neighbor in node.neighbors:
                neighbor_pair = node_pair.get(neighbor.node_id)
                if neighbor_pair is not None and node.node_id in neighbor_pair:
                    continue
                node_pair[node.node_id].append(neighbor.node_id)

        for (node_id, neighbors) in node_pair.items():
            if neighbors.__len__() == 0:
                continue
            for neighbor in neighbors:
                plt.plot([self.nodes[node_id].coordinate.x, self.nodes[neighbor].coordinate.x],
                         [self.nodes[node_id].coordinate.y, self.nodes[neighbor].coordinate.y], '-o')

        plt.show()


def simulation():
    s_config = config.Config()
    thread_pool = []
    for index in range(config.max_index):
        network = Network(s_config.relay_possibility, s_config.peer_size, s_config.neighbor_size)
        network.generate_nodes(s_config.x_start, s_config.x_end, s_config.y_start, s_config.y_end)
        thread = threading.Thread(target=simulate_msgs, args=[network, index])
        thread_pool.append(thread)
        thread.start()
        # simulate_msgs(network, index)
    for thread in thread_pool:
        thread.join()


def simulate_msgs(network, index):
    msg_id = 0
    for neighbor_size in config.neighbor_size_range:
        network.neighbor_size = neighbor_size
        while True:
            network.clear_neighbors()
            network.assign_neighbors()
            if not network.check_is_connected_graph():
                print("generated an unconnected graph, try again")
            else:
                break
        target_time = calculate_target_time(network, index)
        for p in config.p_range:
            network.alpha = p
            network.update_alpha(p)
            for ttl in range(config.ttl_max):
                msg = Message(msg_id, ttl)
                distance = simulate_one_msg(network, index, Message(msg_id, ttl))
                statistics(network, distance, msg, target_time, index)
                network.reset_distance()
                msg_id = msg_id + 1


def calculate_target_time(network, root_index):
    all_nodes = network.nodes
    root_node = all_nodes[root_index]
    distance = dict()
    for node in all_nodes:
        if node.node_id == root_node.node_id:
            distance[node.node_id] = 0
        elif node in root_node.neighbors:
            distance[node.node_id] = root_node.neighbors[node]
        else:
            distance[node.node_id] = graph.max_distance

    received_ids = []
    unreceived_ids = []

    for i in range(all_nodes.__len__()):
        if not i == root_index:
            unreceived_ids.append(i)
        else:
            received_ids.append(i)

    while unreceived_ids.__len__() > 0:
        # find the shortest node
        min_id = -1
        min_dis = graph.max_distance
        for node_id in unreceived_ids:
            if distance[node_id] < min_dis:
                min_id = node_id
                min_dis = distance[node_id]
        # unconnected graph
        if min_id == -1:
            print("index:" + str(root_index) + "  " + str(len(unreceived_ids)) + "error!")
            break
        received_ids.append(min_id)
        unreceived_ids.remove(min_id)

        min_node = all_nodes[min_id]
        for neighbor in min_node.neighbors:
            if distance[neighbor.node_id] > distance[min_id] + min_node.neighbors[neighbor]:
                distance[neighbor.node_id] = distance[min_id] + min_node.neighbors[neighbor]

    max_distance = 0
    for dis in distance.values():
        if dis > max_distance:
            max_distance = dis
    return max_distance


def simulate_one_msg(network, root_index, msg):
    print(str(root_index) + '_' + str(network.neighbor_size) + "_" + str(network.alpha) + "_" + str(msg.ttl) + "_" +
          str(msg.id) + ".json" + " start")
    all_nodes = network.nodes
    root_node = all_nodes[root_index]
    distance = dict()
    path = dict()

    # target_distance = 0
    # init the distance to root node
    for node in all_nodes:
        # dis = root_node.get_distance_of_neighbor(node)
        # if dis > target_distance:
        #     target_distance = dis
        if node.node_id == root_node.node_id:
            distance[node.node_id] = 0
            path[root_node.node_id] = root_node.node_id
        elif node in root_node.neighbors:
            distance[node.node_id] = root_node.neighbors[node]
            path[node.node_id] = root_node.node_id
        else:
            distance[node.node_id] = graph.max_distance
            path[node.node_id] = -1

    received_ids = []
    unreceived_ids = []

    for i in range(all_nodes.__len__()):
        if not i == root_index:
            unreceived_ids.append(i)
        else:
            received_ids.append(i)

    root_node.broadcast_msg(msg)
    while unreceived_ids.__len__() > 0:
        # find the shortest node
        min_id = -1
        min_dis = graph.max_distance
        for node_id in unreceived_ids:
            if distance[node_id] < min_dis:
                min_id = node_id
                min_dis = distance[node_id]
        # unconnected graph
        if min_id == -1:
            print("index:" + str(root_index) + "  " + str(
                len(unreceived_ids)) + " nodes can never receive the message " + str(
                msg.id))
            break
        received_ids.append(min_id)
        unreceived_ids.remove(min_id)

        min_node = all_nodes[min_id]
        min_node.relay_msg(all_nodes[path[min_id]])
        for neighbor in min_node.neighbors:
            if distance[neighbor.node_id] > distance[min_id] + min_node.neighbors[neighbor]:
                distance[neighbor.node_id] = distance[min_id] + min_node.neighbors[neighbor]
                path[neighbor.node_id] = min_id

    return distance


def statistics(network, distance, msg, target_time, root_index):
    all_nodes = network.nodes
    total_redundant = 0
    for node in all_nodes:
        msgs = node.received_msg.get(msg.id)
        if msgs is None:
            continue
        if len(msgs) > 1:
            total_redundant = total_redundant + len(msgs) - 1
    time_array = np.array(list(distance.values()))
    time_array.sort()
    utils.save_result(time_array, total_redundant, network, msg, target_time, root_index)

    # t_end = time_array[len(time_array) - 1]
    # for end in reversed(time_array):
    #     if end != graph.max_distance:
    #         t_end = end
    #         break
    # t_end = int(t_end + 1)
    # t = np.arange(0, t_end, 10)
    # result = []
    # for value in t:
    #     indexes = np.where(time_array > value)
    #     if len(indexes) > 0:
    #         result.append((1 + indexes[0][0]) / len(time_array))

    # print(result[len(result) - 1])
    # print(total_redundant)
    # plt.xlabel("message propagation time")
    # plt.ylabel("message coverage (%)")
    # plt.plot(t, result)
    # plt.legend("upper left")
    # plt.show()


if __name__ == '__main__':
    simulation()
