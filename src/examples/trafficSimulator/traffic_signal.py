class TrafficSignal:
    def __init__(self, roads, config={}):
        # Initialize roads
        self.roads = roads
        # Set default configuration
        self.set_default_config()
        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)
        # Calculate properties
        self.init_properties()
        self.inc = 0
        self.cycle_length = 60

    def set_default_config(self):
        self.cycle = [(False, True), (True, False)]
        self.slow_distance = 50
        self.slow_factor = 0.4
        self.stop_distance = 15

        self.current_cycle_index = 0

        self.last_t = 0

    def init_properties(self):
        for i in range(len(self.roads)):
            for road in self.roads[i]:
                road.set_traffic_signal(self, i)

    @property
    def current_cycle(self):
        return self.cycle[self.current_cycle_index]
    
    def update(self, sim):
        k = (sim.t // self.cycle_length) % 2
        if self.current_cycle_index != int(k):
            cnt_vert = 0
            cnt_hor = 0
            for i in range(len(self.roads)):
                for road in self.roads[i]:
                    if i == 0:
                        cnt_vert += len(road.vehicles)
                    else:
                        cnt_hor += len(road.vehicles)

            cnt_total = [cnt_vert, cnt_hor]
            baseTimer = 80
            timeLimits = [1, 100]
            sum_total = max(sum(cnt_total), 1)

            times = [
                (i / sum_total) * baseTimer
                if timeLimits[0] < (i / sum_total) * baseTimer < timeLimits[1]
                else min(timeLimits, key=lambda x: abs(x - (i / sum_total) * baseTimer))
                for i in cnt_total
            ]
            # Here we update traffic light timer
            # By default 60 seconds
            self.cycle_length = times[int(1-k)]
            print('traffic light time: ', self.cycle_length, ' seconds')

            # TODO total waiting time: 451 minutes. without our logic
            # TODO total waiting time: 412 minutes. with our logic

        self.current_cycle_index = int(k)
