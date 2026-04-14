import simpy
import numpy as np
import random

class Metrics:
    def __init__(self):
        self.total_requests = 0
        self.lost_requests = 0
        self.served_requests = 0
        self.queue_lengths = []
        self.last_time = 0
        self.current_queue_length = 0
        self.busy_time = 0
        self.last_busy_change_time = 0
        self.is_channel_busy = False

        self.waiting_times = []
        self.system_times = []

    def queue_length_snapshot(self, now, new_length):
        delta = now - self.last_time
        if delta > 0:
            self.queue_lengths.append((self.current_queue_length, delta))
        self.current_queue_length = new_length
        self.last_time = now

    def busy_snapshot(self, now, is_busy):
        delta = now - self.last_busy_change_time
        if delta > 0 and self.is_channel_busy:
            self.busy_time += delta
        self.is_channel_busy = is_busy
        self.last_busy_change_time = now

def process_request(
        env: simpy.Environment,
        mu,
        m,
        metrics: Metrics,
        server: simpy.Resource
):
    metrics.total_requests += 1
    arrive_time = env.now
    # current_queue_length = len(server.queue)
    # print(len(server.queue))
    if len(server.queue) >= m:
        metrics.lost_requests += 1
        return
    
    metrics.queue_length_snapshot(env.now, len(server.queue) + 1)

    with server.request() as req:
        start_wait_time = env.now
        yield req
        
        wait_time = env.now - start_wait_time
        metrics.waiting_times.append(wait_time)
        metrics.queue_length_snapshot(env.now, len(server.queue))
        metrics.busy_snapshot(env.now, server.count == 1)
        serv_time = random.expovariate(mu)
        yield env.timeout(serv_time)
        
    metrics.busy_snapshot(env.now, False)
    metrics.served_requests += 1
    system_time = env.now - arrive_time
    metrics.system_times.append(system_time)
    metrics.queue_length_snapshot(env.now, len(server.queue))

def generator(lamd, mu, m, env, metrics, server):
    while True:
        yield env.timeout(random.expovariate(lamd))
        env.process(process_request(env, mu, m, metrics, server))

def calculate_metrics(metrics: Metrics, modeling_time):
    p_loss = metrics.lost_requests / metrics.total_requests
    summa = 0
    for elem in metrics.queue_lengths:
        summa += elem[0] * elem[1]
    l_q = summa / modeling_time
    w_q = np.mean(metrics.waiting_times) if metrics.waiting_times else 0
    w_s = np.mean(metrics.system_times) if metrics.system_times else 0
    rho = metrics.busy_time / modeling_time

    return {
        "Вероятность потери заявок (модель)": p_loss,
        "Среднее число заявок в очереди (модель)": l_q,
        "Среднее время ожидания заявки в очереди (модель)": w_q,
        "Среднее время пребывания заявки в системе (модель)": w_s,
        "Коэффициент загрузки системы (модель)": rho
    }

def run_modeling(lamd, mu, m, modeling_time):
    env = simpy.Environment()
    server = simpy.Resource(env, capacity=1)
    metrics = Metrics()
    env.process(generator(lamd, mu, m, env, metrics, server))
    env.run(until=modeling_time)
    if metrics.is_channel_busy:
        metrics.busy_time += env.now - metrics.last_busy_change_time

    return calculate_metrics(metrics, modeling_time)
