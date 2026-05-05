import simpy
import numpy as np
import random

class Metrics:
    def __init__(self):
        self.total_requests = 0
        self.lost_requests = 0
        self.served_requests = 0

        self.waiting_times = []
        self.system_times = []

        self.queue_lengths = []
        self.current_queue = 0
        self.last_time = 0

        self.agent_stats = []
        self.current_agents = 0
        self.last_agents_time = 0

    def queue_snapshot(self, now, new_len):
        dt = now - self.last_time
        if dt > 0:
            self.queue_lengths.append((self.current_queue, dt))
        self.current_queue = new_len
        self.last_time = now

    def agents_snapshot(self, now, new_agents):
        dt = now - self.last_agents_time
        if dt > 0:
            self.agent_stats.append((self.current_agents, dt))
        self.current_agents = new_agents
        self.last_agents_time = now

class Node:
    def __init__(
            self,
            env,
            mu,
            init_value,
            max_queue=10,
            max_agents=5,
            min_agents=1,
            lambda_on=1.0,
            lambda_off=0.5
    ):
        self.env = env
        self.mu = mu

        self.agents = simpy.Container(env, init=init_value, capacity=max_agents)

        self.queue = []
        self.max_queue = max_queue

        self.lambda_on = lambda_on
        self.lambda_off = lambda_off

        self.waiting_times = []

        self.queue_lengths = []
        self.current_queue = 0
        self.last_time = 0

        self.agent_stats = []
        self.current_agents = min_agents
        self.last_agents_time = 0

    def queue_snapshot(self, now, new_len):
        dt = now - self.last_time
        if dt > 0:
            self.queue_lengths.append((self.current_queue, dt))
        self.current_queue = new_len
        self.last_time = now

    def agents_snapshot(self, now, new_agents):
        dt = now - self.last_agents_time
        if dt > 0:
            self.agent_stats.append((self.current_agents, dt))
        self.current_agents = new_agents
        self.last_agents_time = now

def process_request(env, node_name, nodes, routing, metrics: Metrics):
    metrics.total_requests += 1
    arrival_time = env.now

    current_node = node_name

    while current_node is not None:
        node = nodes[current_node]

        if len(node.queue) >= node.max_queue:
            metrics.lost_requests += 1
            return

        node.queue.append(1)
        metrics.queue_snapshot(env.now, len(node.queue))
        node.queue_snapshot(env.now, len(node.queue))

        start_wait = env.now

        yield node.agents.get(1)

        wait_time = env.now - start_wait

        metrics.waiting_times.append(wait_time)
        node.waiting_times.append(wait_time)

        node.queue.pop(0)

        metrics.queue_snapshot(env.now, len(node.queue))
        node.queue_snapshot(env.now, len(node.queue))

        service_time = random.expovariate(node.mu)
        yield env.timeout(service_time)

        yield node.agents.put(1)

        current_node = route(routing[current_node])

    metrics.served_requests += 1
    metrics.system_times.append(env.now - arrival_time)

def route(transitions):
    r = random.random()
    cumulative = 0

    for node, prob in transitions:
        cumulative += prob
        if r <= cumulative:
            return node

    return None

def generator(env, lamd, nodes, routing, metrics):
    while True:
        yield env.timeout(random.expovariate(lamd))
        env.process(process_request(env, "node1", nodes, routing, metrics))

def agent_manager(env, node: Node, metrics: Metrics):
    print("here")
    while True:
        total = node.lambda_on + node.lambda_off
        yield env.timeout(random.expovariate(total))

        if random.random() < node.lambda_on / total:
            if node.agents.level < node.agents.capacity:
                yield node.agents.put(1)

                metrics.agents_snapshot(env.now, node.agents.level)
                node.agents_snapshot(env.now, node.agents.level)
        else:
            if node.agents.level > 1:
                yield node.agents.get(1)

                metrics.agents_snapshot(env.now, node.agents.level)
                node.agents_snapshot(env.now, node.agents.level)


def calculate(metrics: Metrics, modeling_time):
    p_loss = metrics.lost_requests / metrics.total_requests if metrics.total_requests else 0

    Lq = sum(q * t for q, t in metrics.queue_lengths) / modeling_time if metrics.queue_lengths else 0
    Wq = np.mean(metrics.waiting_times) if metrics.waiting_times else 0
    Ws = np.mean(metrics.system_times) if metrics.system_times else 0

    La = sum(a * t for a, t in metrics.agent_stats) / modeling_time if metrics.agent_stats else 0

    return {
        "P_loss": p_loss,
        "Lq": Lq,
        "Wq": Wq,
        "Ws": Ws,
        "Avg_agents": La
    }


def calculate_node(node: Node, modeling_time):
    Lq = sum(q * t for q, t in node.queue_lengths) / modeling_time if node.queue_lengths else 0
    Wq = np.mean(node.waiting_times) if node.waiting_times else 0
    La = sum(a * t for a, t in node.agent_stats) / modeling_time if node.agent_stats else 0

    return {
        "Lq": Lq,
        "Wq": Wq,
        "Avg_agents": La
    }

def run_model_with_params(node_names, lambd, fixed_value, lambda_on, lambda_off):
    print(node_names, lambd, lambda_on)
    env = simpy.Environment()
    metrics = Metrics()

    init_values = [3, 2, 2, 3, 2]
    if fixed_value != None:
        init_values[int(node_names[0][-1]) - 1] = fixed_value

    nodes = {
        "node1": Node(env, mu=220, init_value=init_values[0], min_agents=1, max_agents=5),
        "node2": Node(env, mu=50, init_value=init_values[1], min_agents=1, max_agents=3),
        "node3": Node(env, mu=70, init_value=init_values[2], min_agents=1, max_agents=2),
        "node4": Node(env, mu=60, init_value=init_values[3], min_agents=1, max_agents=4),
        "node5": Node(env, mu=200, init_value=init_values[4], min_agents=1, max_agents=3),
    }

    for node_name in node_names:
        nodes[node_name].lambda_on = lambda_on
        nodes[node_name].lambda_off = lambda_off

    routing = {
        "node1": [("node2", 0.3), ("node3", 0.3), ("node4", 0.4)],
        "node2": [("node3", 0.3), ("node4", 0.7)],
        "node3": [("node4", 1.0)],
        "node4": [("node5", 1.0)],
        "node5": [(None, 1.0)]
    }

    env.process(generator(env, lambd, nodes, routing, metrics))

    for key, node in nodes.items():
        if key in node_names and fixed_value == None:
            env.process(agent_manager(env, node, metrics))

    env.run(until=1000)

    global_metrics = calculate(metrics, 1000)

    node_metrics = {
        name: calculate_node(node, 1000)
        for name, node in nodes.items()
    }

    return {
        "global": global_metrics,
        "nodes": node_metrics
    }
