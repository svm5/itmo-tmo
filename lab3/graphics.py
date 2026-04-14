import matplotlib.pyplot as plt

from task import run_modeling

lamd = 3
mu = 4
m_values = [i for i in range(2, 10)]
modeling_time = 2000
p_losses = []
w_q = []
for m_value in m_values:
    metrics = run_modeling(lamd, mu, m_value, modeling_time)
    p_losses.append(metrics["Вероятность потери заявок (модель)"])
    w_q.append(metrics["Среднее время ожидания заявки в очереди (модель)"])

fig, axes = plt.subplots(1, 2, figsize=(10, 8))
axes[0].plot(m_values, p_losses, marker="o")
axes[0].grid()
axes[0].set_xlabel("Максимальная длина очереди")
axes[0].set_ylabel("Вероятность потерь")
axes[1].plot(m_values, w_q, marker="o")
axes[1].grid()
axes[1].set_xlabel("Максимальная длина очереди")
axes[1].set_ylabel("Среднее время ожидания в очереди (мин)")
plt.show()
