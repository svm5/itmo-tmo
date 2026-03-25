import numpy as np

class Generator:
    def __init__(self, flow_intensity, service_intensity):
        self.flow_intensity = flow_intensity
        self.service_intensity = service_intensity

    def generateTwoRequestsComeInterval(self):
        return np.random.exponential(scale=1/self.flow_intensity)
    
    def generateServeTime(self):
        return np.random.exponential(scale=1/self.service_intensity)
    
class ModelingSystem:
    def __init__(self, channels_count):
        self.channels_count = channels_count
        self.channels = [0 for _ in range(channels_count)]
        self.queue = []

        self.clear()        

    def clear(self):
        for i in range(self.channels_count):
            self.channels[i] = 0
        self.queue = []

        self.queue_length_history = []
        self.busy_channels_history = []
        self.last_time = 0
        self.requests_amount = 0
        self.total_queue_time = 0
        self.total_system_time = 0
        self.max_time = 0

    def addRequest(self, arrival_time, service_duration):
        self.updateSystemState(arrival_time)
        
        for i in range(self.channels_count):
            if self.channels[i] <= arrival_time:
                self.channels[i] = arrival_time + service_duration
                
                self.requests_amount += 1
                self.total_system_time += service_duration
                
                self.max_time = max(self.max_time, self.channels[i])
                return True
        
        self.queue.append((arrival_time, service_duration))
        return False
    
    def updateSystemState(self, current_time):
        while True:
            next_event = min(self.channels)
            if next_event <= self.last_time or next_event > current_time:
                break
            
            self.makeSnapshot(next_event)
            self.processQueue(next_event)
        
        self.makeSnapshot(current_time)
        self.processQueue(current_time)
    
    def processQueue(self, current_time):
        while len(self.queue) > 0:
            free_channels = [i for i in range(self.channels_count) if self.channels[i] <= current_time]
            if not free_channels:
                break
            for i in free_channels:
                if not self.queue:
                    break
                
                arrival_time, service_duration = self.queue.pop(0)
                wait_time = current_time - arrival_time
                
                self.requests_amount += 1
                self.total_queue_time += wait_time
                self.total_system_time += wait_time + service_duration
                
                self.channels[i] = current_time + service_duration
                self.max_time = max(self.max_time, self.channels[i])

    def makeSnapshot(self, current_time):
        if len(self.queue_length_history) > 0 and current_time == self.queue_length_history[-1][0]:
            return
            
        queue_length = len(self.queue)
        self.queue_length_history.append((current_time, queue_length))

        busy_count = 0
        for t_free in self.channels:
            if t_free > current_time:
                busy_count += 1
        self.busy_channels_history.append((current_time, busy_count))
        self.last_time = current_time

    def finalize(self, end_time):
        self.updateSystemState(end_time)
        self.makeSnapshot(end_time)
        self.max_time = max(self.max_time, end_time)

    def calculateDowntimeProbability(self):
        if not self.busy_channels_history or self.max_time == 0:
            return 0
            
        downtime = 0
        prev_time = self.busy_channels_history[0][0]
        prev_busy = self.busy_channels_history[0][1]

        for i in range(1, len(self.busy_channels_history)):
            current_time = self.busy_channels_history[i][0]
            current_busy = self.busy_channels_history[i][1]
            if prev_busy == 0:
                downtime += current_time - prev_time
            prev_time = current_time
            prev_busy = current_busy

        if prev_busy == 0:
            downtime += self.max_time - prev_time
        
        return downtime / self.max_time

    def queueWaitProbability(self):
        if not self.busy_channels_history or self.max_time == 0:
            return 0
            
        all_queue_time = 0
        prev_time = self.busy_channels_history[0][0]
        prev_busy = self.busy_channels_history[0][1]

        for i in range(1, len(self.busy_channels_history)):
            current_time = self.busy_channels_history[i][0]
            current_busy = self.busy_channels_history[i][1]
            if prev_busy == self.channels_count:
                all_queue_time += current_time - prev_time
            prev_time = current_time
            prev_busy = current_busy
        
        if prev_busy == self.channels_count:
            all_queue_time += self.max_time - prev_time

        return all_queue_time / self.max_time
    
    def calculateAverageRequestsInQueueCount(self):
        if not self.queue_length_history or self.max_time == 0:
            return 0
            
        weighted_sum = 0
        prev_time = self.queue_length_history[0][0]
        prev_length = self.queue_length_history[0][1]

        for i in range(1, len(self.queue_length_history)):
            current_time = self.queue_length_history[i][0]
            current_length = self.queue_length_history[i][1]
            weighted_sum += prev_length * (current_time - prev_time)
            prev_time = current_time
            prev_length = current_length
        
        weighted_sum += prev_length * (self.max_time - prev_time)
        return weighted_sum / self.max_time
    
    def calculateAverageRequestInQueueTime(self):
        if self.requests_amount == 0:
            return 0
        return self.total_queue_time / self.requests_amount
    
    def calculateAverageRequestTime(self):
        if self.requests_amount == 0:
            return 0
        return self.total_system_time / self.requests_amount
    
    def calculateLoadCoefficient(self):
        if not self.busy_channels_history or self.max_time == 0:
            return 0
            
        weighted_sum = 0
        prev_time = self.busy_channels_history[0][0]
        prev_busy = self.busy_channels_history[0][1]

        for i in range(1, len(self.busy_channels_history)):
            current_time = self.busy_channels_history[i][0]
            current_busy = self.busy_channels_history[i][1]
            weighted_sum += prev_busy * (current_time - prev_time)
            prev_time = current_time
            prev_busy = current_busy
        
        weighted_sum += prev_busy * (self.max_time - prev_time)
        return weighted_sum / (self.max_time * self.channels_count)

class PassengerBoardingModel:
    def __init__(self, flow_intensity, service_intensity, channels_amount, modeling_time):
        self.flow_intensity = flow_intensity
        self.service_intensity = service_intensity
        self.time = modeling_time
        self.system = ModelingSystem(channels_amount)

    def run(self):
        generator = Generator(self.flow_intensity, self.service_intensity)
        self.system.clear()
        
        current_time = 0
        while current_time < self.time:
            interval = generator.generateTwoRequestsComeInterval()
            next_arrival = current_time + interval
            
            if next_arrival >= self.time:
                break
  
            service_time = generator.generateServeTime()
            self.system.addRequest(next_arrival, service_time)
            current_time = next_arrival

        self.system.finalize(self.time)
