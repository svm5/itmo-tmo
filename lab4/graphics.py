import matplotlib.pyplot as plt

from calculate_theory import calculate_theory
from task import start_model

lambda1 = 5
lambda2 = 30
lambda1_values = [i for i in range(3, 10, 1)]
lambda2_values = [i for i in range(25, 35, 1)]
mu = 60

lambda1_model_values_w1 = []
lambda1_th_values_w1 = []
lambda1_model_values_w2 = []
lambda1_th_values_w2 = []

lambda2_model_values_w1 = []
lambda2_th_values_w1 = []
lambda2_model_values_w2 = []
lambda2_th_values_w2 = []
for lambda1_value in lambda1_values:
    a = start_model(lambda1_value, lambda2, mu, 2000, 0)
    b = calculate_theory(lambda1_value, lambda2, mu)
    lambda1_model_values_w1.append(a["w1"])
    lambda1_th_values_w1.append(b["w1"])
    lambda1_model_values_w2.append(a["w2"])
    lambda1_th_values_w2.append(b["w2"])

for lambda2_value in lambda2_values:
    a = start_model(lambda1, lambda2_value, mu, 2000, 0)
    b = calculate_theory(lambda1, lambda2_value, mu)
    lambda2_model_values_w1.append(a["w1"])
    lambda2_th_values_w1.append(b["w1"])
    lambda2_model_values_w2.append(a["w2"])
    lambda2_th_values_w2.append(b["w2"])
    

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0, 0].plot(lambda1_values, lambda1_model_values_w1, label="Модель")
axes[0, 0].plot(lambda1_values, lambda1_th_values_w1, label="Теория")
axes[0, 0].set_xlabel("Итенсивность входящего высокоприоритетного потока (чел/час)")
axes[0, 0].set_ylabel("Время ожидания в очереди\nвысокоприоритетных заявок")
axes[0, 0].grid()
axes[0, 0].legend()
axes[0, 1].plot(lambda1_values, lambda1_model_values_w2, label="Модель")
axes[0, 1].plot(lambda1_values, lambda1_th_values_w2, label="Теория")
axes[0, 1].set_xlabel("Итенсивность входящего высокоприоритетного потока (чел/час)")
axes[0, 1].set_ylabel("Время ожидания в очереди\nнизкоприоритетных заявок")
axes[0, 1].grid()
axes[0, 1].legend()

axes[1, 0].plot(lambda2_values, lambda2_model_values_w1, label="Модель")
axes[1, 0].plot(lambda2_values, lambda2_th_values_w1, label="Теория")
axes[1, 0].set_xlabel("Итенсивность входящего низкоприоритетного потока (чел/час)")
axes[1, 0].set_ylabel("Время ожидания в очереди\nвысокоприоритетных заявок")
axes[1, 0].grid()
axes[1, 0].legend()
axes[1, 1].plot(lambda2_values, lambda2_model_values_w2, label="Модель")
axes[1, 1].plot(lambda2_values, lambda2_th_values_w2, label="Теория")
axes[1, 1].set_xlabel("Итенсивность входящего низкоприоритетного потока (чел/час)")
axes[1, 1].set_ylabel("Время ожидания в очереди\nнизкоприоритетных заявок")
axes[1, 1].grid()
axes[1, 1].legend()
plt.show()
