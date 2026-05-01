import numpy as np
import heapq
from dataclasses import dataclass
from collections import deque

@dataclass
class Request:
    id: int
    priority: str
    arrive_time: float
    service_time: float
    remaining_time: float
    start_time: float = None
    finish_time: float = None
    total_wait_time: float = 0
    last_queue_enter_time: float = 0
    
    recorded: bool = False


class PriorityQueueSystem:
    def __init__(self, lam_high, lam_low, mu, T, warmup=0):
        self.lam_high = lam_high
        self.lam_low = lam_low
        self.mu = mu
        self.T = T
        self.warmup = warmup
        self.event_queue = []
        self.time = 0
        self.server_busy = False
        self.current = None
        self.high_q = deque()
        self.low_q = deque()
        self.req_id = 0

        self.high_wait = []
        self.high_sys = []
        self.high_wait_flag = []
        self.low_wait = []
        self.low_sys = []
        self.low_wait_flag = []
        self.busy_time = 0
        self.last_start = None
        self.requests_sum = 0
        self.last_event_time = 0

    def schedule(self, t, event_type, data):
        heapq.heappush(self.event_queue, (t, event_type, data))

    def exp(self, rate):
        return np.random.exponential(1 / rate)

    def make_snapshot(self):
        dt = self.time - self.last_event_time
        if self.time >= self.warmup:
            n = len(self.high_q) + len(self.low_q) + (1 if self.server_busy else 0)
            self.requests_sum += n * dt
        self.last_event_time = self.time

    def arrival(self, req):
        req.last_queue_enter_time = self.time
        if req.priority == 'high' and self.server_busy and self.current.priority == 'low':
            elapsed = self.time - self.last_start
            self.current.remaining_time = max(0.0, self.current.remaining_time - elapsed)
            self.current.last_queue_enter_time = self.time
            self.low_q.append(self.current)
            if self.time >= self.warmup:
                self.busy_time += elapsed
            self.server_busy = False
            self.current = None

        if req.priority == 'high':
            self.high_q.append(req)
        else:
            self.low_q.append(req)

        self.try_start()

    def try_start(self):
        if self.server_busy:
            return

        if self.high_q:
            req = self.high_q.popleft()
        elif self.low_q:
            req = self.low_q.popleft()
        else:
            return

        wait = self.time - req.last_queue_enter_time
        req.total_wait_time += wait

        if not req.recorded and self.time >= self.warmup:
            req.recorded = True
            if req.priority == 'high':
                self.high_wait_flag.append(wait > 1e-10)
            else:
                self.low_wait_flag.append(wait > 1e-10)

        req.start_time = self.time

        self.server_busy = True
        self.current = req
        self.last_start = self.time

        finish = self.time + max(req.remaining_time, 1e-12)
        self.schedule(finish, 'departure', req)

    def departure(self, req):
        if req is not self.current:
            return
        elapsed = self.time - self.last_start
        if self.time >= self.warmup:
            self.busy_time += elapsed
        req.finish_time = self.time
        sys_time = self.time - req.arrive_time

        if self.time >= self.warmup:
            if req.priority == 'high':
                self.high_wait.append(req.total_wait_time)
                self.high_sys.append(sys_time)
            else:
                self.low_wait.append(req.total_wait_time)
                self.low_sys.append(sys_time)

        self.server_busy = False
        self.current = None

        self.try_start()

    def run(self):
        self.schedule(self.exp(self.lam_high), 'arrival', 'high')
        self.schedule(self.exp(self.lam_low), 'arrival', 'low')

        arrivals_stopped = False
        while self.event_queue:
            t, event, data = heapq.heappop(self.event_queue)
            self.time = t
            self.make_snapshot()
            if self.time >= self.T:
                arrivals_stopped = True
            if event == 'arrival':
                if arrivals_stopped:
                    continue

                priority = data
                service_time = self.exp(self.mu)
                req = Request(
                    id=self.req_id,
                    priority=priority,
                    arrive_time=self.time,
                    service_time=service_time,
                    remaining_time=service_time
                )

                self.req_id += 1
                self.arrival(req)
                next_time = self.time + self.exp(
                    self.lam_high if priority == 'high' else self.lam_low
                )
                if not arrivals_stopped:
                    self.schedule(next_time, 'arrival', priority)

            else:
                self.departure(data)

            if arrivals_stopped and not self.server_busy and not self.high_q and not self.low_q:
                break

        total_time = self.time - self.warmup

        return {
            "w1": np.mean(self.high_wait),
            "w2": np.mean(self.low_wait),
            "t1": np.mean(self.high_sys),
            "t2": np.mean(self.low_sys),
            "p1": np.mean(self.high_wait_flag),
            "p2": np.mean(self.low_wait_flag),
            "rho": self.busy_time / total_time,
            "avg": self.requests_sum / total_time
        }

def start_model(lambda1, lambda2, mu, T=100000, warmup=20000, seed=42):
    # np.random.seed(seed)

    model = PriorityQueueSystem(lambda1, lambda2, mu, T, warmup)
    result = model.run()
    return result
