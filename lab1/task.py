import numpy as np

class Generator:
    def __init__(self, flow_intensity, service_intensity):
        self.flow_intensity = flow_intensity
        self.service_intensity = service_intensity

    def generateTwoRequestsComeInterval(self):
        return np.random.exponential(scale=1/self.flow_intensity)
    
    def generateServeTime(self):
        return np.random.exponential(scale=1/self.service_intensity)

class Calculator:
    def __init__(self, flow_intensity, service_intensity):
        self.flow_intensity = flow_intensity
        self.service_intensity = service_intensity

    def calculateRejectProbabilityForOneChannelSystem(self):
        return self.flow_intensity / (self.flow_intensity + self.service_intensity)

class ModelingSystem:
    def __init__(self, channels_count, queue_capacity):
        self.channels_count = channels_count
        self.channels = [0 for _ in range(channels_count)]
        self.queue_capacity = queue_capacity

    def clear(self):
        for i in range(self.channels_count):
            self.channels[i] = 0

    def tryAddToChannel(self, begin, duration):
        for i in range(self.channels_count):
            if self.channels[i] <= begin:
                self.channels[i] = begin + duration
                return True
            
        return False

class PassengerBoardingModel:
    def __init__(self, flow_intensity, service_intensity, modeling_time):
        self.flow_intensity = flow_intensity
        self.service_intensity = service_intensity
        self.time = modeling_time
        
        self.system = ModelingSystem(1, 0)
        
        self.incoming_requests = 0
        self.served_requests = 0
        self.lost_requests = 0
        self.channel_busy_time = 0

    def run(self):
        generator = Generator(self.flow_intensity, self.service_intensity)
        self.system.clear()

        current_time = 0
        while current_time < self.time:
            next_come = current_time + generator.generateTwoRequestsComeInterval()
            self.incoming_requests += 1
            if next_come >= self.time:
                break
            current_serve_time = generator.generateServeTime()
            if self.system.tryAddToChannel(next_come, current_serve_time):
                self.served_requests += 1
                self.channel_busy_time += current_serve_time
            else:
                self.lost_requests += 1
            current_time = next_come
    
    def getRejectProbability(self):
        if self.incoming_requests == 0:
            return 0
        
        return self.lost_requests / self.incoming_requests

