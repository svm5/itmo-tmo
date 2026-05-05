import matplotlib.pyplot as plt
from task import run_model_with_params
import pprint

# 1 - для каждой ноды динамически меняем число каналов, остальные fixe

nodes = ["node1", "node2", "node3", "node4", "node5"]
lambda_on_values = [0.2, 0.5, 1]
results_1_global = {}
results_1 = {}
for node in nodes:
    results_1[node] = []
    results_1_global[node] = []
    for lambda_on_value in lambda_on_values:
        result = run_model_with_params(
            node_names=[node],
            lambd=150,
            fixed_value=None,
            lambda_on=lambda_on_value,
            lambda_off=0.5
        )
        # pprint.pprint(result["global"])
        # pprint.pprint(result["nodes"][node])
        results_1_global[node].append(result["global"])
        results_1[node].append(result["nodes"][node])
        pprint.pprint(result)

node_names = {
    0: "Узел 1 - Вход",
    1: "Узел 2 - Касса продажи билетов",
    2: "Узел 3 - Досмотр",
    3: "Узел 4 - Турникеты",
    4: "Узел 5 - Посадка в автобус"
}

fig, axes = plt.subplots(2, 3, figsize=(10, 8))
for i, node in enumerate(nodes):
    wq_values = []
    for data in results_1[node]:
        wq_values.append(data["Wq"])
    axes[0, 0].plot(lambda_on_values, wq_values, label=node, marker='o')
axes[0, 0].set_xlabel("lambda_on")
axes[0, 0].set_ylabel("Wq")
axes[0, 0].set_title("Время ожидания в очереди в ноде")
axes[0, 0].grid()
axes[0, 0].legend()

for i, node in enumerate(nodes):
    wq_values = []
    for data in results_1_global[node]:
        wq_values.append(data["Wq"])
    axes[0, 1].plot(lambda_on_values, wq_values, label=node, marker='o')
axes[0, 1].set_xlabel("lambda_on")
axes[0, 1].set_ylabel("Wq")
axes[0, 1].set_title("Глобальное время ожидания в очереди")
axes[0, 1].grid()
axes[0, 1].legend()

for i, node in enumerate(nodes):
    ws_values = []
    for data in results_1_global[node]:
        ws_values.append(data["Ws"])
    axes[0, 2].plot(lambda_on_values, ws_values, label=node, marker='o')
axes[0, 2].set_xlabel("lambda_on")
axes[0, 2].set_ylabel("Ws")
axes[0, 2].set_title("Время нахождения заявки в системе")
axes[0, 2].grid()
axes[0, 2].legend()

for i, node in enumerate(nodes):
    wq_values = []
    for data in results_1[node]:
        wq_values.append(data["Lq"])
    axes[1, 0].plot(lambda_on_values, wq_values, label=node, marker='o')
axes[1, 0].set_xlabel("lamnda_on")
axes[1, 0].set_ylabel("Lq")
axes[1, 0].set_title("Длина очереди в ноде")
axes[1, 0].grid()
axes[1, 0].legend()

for i, node in enumerate(nodes):
    wq_values = []
    for data in results_1_global[node]:
        wq_values.append(data["Lq"])
    axes[1, 1].plot(lambda_on_values, wq_values, label=node, marker='o')
axes[1, 1].set_xlabel("lamnda_on")
axes[1, 1].set_ylabel("Lq")
axes[1, 1].set_title("Глобальная длина очереди")
axes[1, 1].grid()
axes[1, 1].legend()


plt.tight_layout()
plt.show()



# 2 - фиксируем для каждой ноды
nodes_channels_variants = [5, 3, 2, 4, 3]
results_2_global = {}
results_2 = {}
for i in range(len(nodes)):
    results_2[nodes[i]] = []
    results_2_global[nodes[i]] = []
    for j in range(1, nodes_channels_variants[i] + 1):
        result = run_model_with_params(
            node_names=[nodes[i]],
            lambd=150,
            fixed_value=j,
            lambda_on=1.0, # don't use
            lambda_off=0.5 # don't  use
        )
        pprint.pprint(result)
        results_2[nodes[i]].append(result["nodes"][nodes[i]])
        results_2_global[nodes[i]].append(result["global"])
    

for i in range(len(nodes)):
    fig, axes = plt.subplots(2, 3, figsize=(10, 8))
    fig.suptitle(node_names[i])
    wq_values = []
    wq_values_global = []
    lq_values = []
    lq_values_global = []
    ws_values = []
    for data in results_2[nodes[i]]:
        wq_values.append(data["Wq"])
        lq_values.append(data["Lq"])
    for data in results_2_global[nodes[i]]:
        wq_values_global.append(data["Wq"])
        lq_values_global.append(data["Lq"])
        ws_values.append(data["Ws"])

    axes[0, 0].plot([k + 1 for k in range(nodes_channels_variants[i])], wq_values, marker='o')
    axes[0, 1].plot([k + 1 for k in range(nodes_channels_variants[i])], wq_values_global, marker='o')
    axes[0, 2].plot([k + 1 for k in range(nodes_channels_variants[i])], ws_values, marker='o')
    axes[1, 0].plot([k + 1 for k in range(nodes_channels_variants[i])], lq_values, marker='o')
    axes[1, 1].plot([k + 1 for k in range(nodes_channels_variants[i])], lq_values_global, marker='o')
    
    axes[0, 0].grid()
    axes[0, 0].set_xlabel("Число активных агентов")
    axes[0, 0].set_ylabel("Wq")
    axes[0, 0].set_title("Глобальное время ожидания в очереди")

    axes[0, 1].grid()
    axes[0, 1].set_xlabel("Число активных агентов")
    axes[0, 1].set_ylabel("Wq")
    axes[0, 1].set_title("Время ожидания в очереди в ноде")

    axes[0, 2].grid()
    axes[0, 2].set_xlabel("Число активных агентов")
    axes[0, 2].set_ylabel("Ws")
    axes[0, 2].set_title("Время нахождения заявки в системе")

    axes[1, 0].grid()
    axes[1, 0].set_xlabel("Число активных агентов")
    axes[1, 0].set_ylabel("Lq")
    axes[1, 0].set_title("Длина очереди в ноде")

    axes[1, 1].grid()
    axes[1, 1].set_xlabel("Число активных агентов")
    axes[1, 1].set_ylabel("Lq")
    axes[1, 1].set_title("Глобальная длина очереди в системе")

    plt.tight_layout()
    plt.show()
