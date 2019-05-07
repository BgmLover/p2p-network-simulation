class Config:
    def __init__(self):
        # graph config
        self.x_start = 0
        self.x_end = 1000
        self.y_start = 0
        self.y_end = 1000

        # p2p config
        self.peer_size = 1000
        self.neighbor_size = 8
        self.relay_possibility = 0.3
        self.ttl = 0


# save dir
save_dir = "data/"

neighbor_size_range = [7, 8, 9, 10, 11, 12, 13, 14, 15]
p_range = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
delay_range = [0.05, 0.6]  # 0.05s -- 0.6s
levelset_size = 1000 * 0.5 * 7  # 3500kB
block_size = 0.5  # 0.5 kB
speed_range = [1 * 1000, 10 * 1000]  # 1M/s -- 10M/s
transfer_time_range = [0.05, 0.35]  # 0.35s -- 3.5s

target_time = 6  # 6s
ttl_max = 10
max_index = 100

show_log = True
