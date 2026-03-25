import matplotlib.pyplot as plt
from math import factorial
import numpy as np

from task import PassengerBoardingModel

def calculateDowntimeProbability(lambd, mu, n):
    res = 0
    for i in range(0, n + 1):
        res += (lambd / mu) ** i / factorial(i)
    res += (lambd / mu) ** (n + 1) / factorial(n) * (n - lambd / mu)
    
    return res ** (-1)

def queueWaitProbability(lambd, mu, n):
    return (lambd / mu) ** (n + 1) / (factorial(n) * (n - lambd / mu)) * calculateDowntimeProbability(lambd, mu, n)

def calculateAverageRequestsInQueueCount(lambd, mu, n):
    return n / (n - lambd / mu) * queueWaitProbability(lambd, mu, n)

def calculateAverageRequestInQueueTime(lambd, mu, n):
    return calculateAverageRequestsInQueueCount(lambd, mu, n) / lambd

def calculateAverageRequestTime(lambd, mu, n):
    return calculateAverageRequestInQueueTime(lambd, mu, n) + 1 / mu

def calculateLoadCoefficient(lambd, mu, n):
    return lambd / (mu * n)

fixed_lambda = 60
fixed_mu_value = 40
fixed_channels_count = 2
channels_count = [i for i in range(2, 7)]
mu_values = [i for i in range(20, 10, 70)]

experiment_result_channels_avarage_wait_time = []
theory_result_channels_avarage_wait_time = []
experiment_result_channels_avarage_queue_length = []
theory_result_channels_avarage_queue_length = []
for current_channel_count in channels_count:
    model = PassengerBoardingModel(fixed_lambda, fixed_mu_value, current_channel_count, 1000)
    model.run()
    experiment_result_channels_avarage_wait_time.append(model.system.calculateAverageRequestInQueueTime())
    experiment_result_channels_avarage_queue_length.append(model.system.calculateAverageRequestsInQueueCount())

    theory_result_channels_avarage_wait_time.append(calculateAverageRequestInQueueTime(fixed_lambda, fixed_mu_value, current_channel_count))
    theory_result_channels_avarage_queue_length.append(calculateAverageRequestsInQueueCount(fixed_lambda, fixed_mu_value, current_channel_count))

experiment_result_mu_avarage_wait_time = []
theory_result_mu_avarage_wait_time = []
experiment_result_mu_avarage_queue_length = []
theory_result_mu_avarage_queue_length = []
mu_values = [i for i in range(40, 75, 5)]
for mu in mu_values:
    model = PassengerBoardingModel(fixed_lambda, mu, fixed_channels_count, 1000)
    model.run()
    experiment_result_mu_avarage_wait_time.append(model.system.calculateAverageRequestInQueueTime())
    experiment_result_mu_avarage_queue_length.append(model.system.calculateAverageRequestsInQueueCount())

    theory_result_mu_avarage_wait_time.append(calculateAverageRequestInQueueTime(fixed_lambda, mu, fixed_channels_count))
    theory_result_mu_avarage_queue_length.append(calculateAverageRequestsInQueueCount(fixed_lambda, mu, fixed_channels_count))

fig, axes = plt.subplots(2, 2, figsize=(10, 8))

axes[0, 0].plot(channels_count, experiment_result_channels_avarage_wait_time, marker="o", label="Среднее время ожидания (эксп)")
axes[0, 1].plot(channels_count, experiment_result_channels_avarage_queue_length, marker="o", label="Средняя длина очереди (эксп)")
axes[0, 0].plot(channels_count, theory_result_channels_avarage_wait_time, marker="o", label="Среднее время ожидания (теор)")
axes[0, 1].plot(channels_count, theory_result_channels_avarage_queue_length, marker="o", label="Средняя длина очереди (теор)")
axes[0, 0].set_xlabel("Число каналов")
axes[0, 0].set_ylabel("Среднее время ожидания (часы)")
axes[0, 1].set_xlabel("Число каналов")
axes[0, 1].set_ylabel("Количество человек в очереди")
axes[0, 0].grid()
axes[0, 1].grid()
axes[0, 0].legend()
axes[0, 1].legend()

axes[1, 0].plot(mu_values, experiment_result_mu_avarage_wait_time, marker="o", label="Среднее время ожидания")
axes[1, 1].plot(mu_values, experiment_result_mu_avarage_queue_length, marker="o", label="Средняя длина очереди")
axes[1, 0].plot(mu_values, theory_result_mu_avarage_wait_time, marker="o", label="Среднее время ожидания (теор)")
axes[1, 1].plot(mu_values, theory_result_mu_avarage_queue_length, marker="o", label="Средняя длина очереди (теор)")
axes[1, 0].set_xlabel("Интенсивность обслуживания")
axes[1, 0].set_ylabel("Среднее время ожидания (часы)")
axes[1, 1].set_xlabel("Интенсивность обслуживания")
axes[1, 1].set_ylabel("Количество человек в очереди")
axes[1, 0].grid()
axes[1, 1].grid()
axes[1, 0].legend()
axes[1, 1].legend()

plt.show()
