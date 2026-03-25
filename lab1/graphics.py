import matplotlib.pyplot as plt

from task import PassengerBoardingModel

mu_value = 20
lambda_values = [i for i in range(1, mu_value * 3 + 1)]
experiment_result = []
theory_result = []
for val in lambda_values:
    model = PassengerBoardingModel(val, mu_value, 1000)
    model.run()
    experiment_result.append(model.getRejectProbability())
    theory_result.append(val / (val + mu_value))

    print(f"lambda: {val}, mu: {mu_value}", end=" ")
    print(f"Всего заявок: {model.incoming_requests}", end=" ")
    print(f"Обсуженных: {model.served_requests}", end=" ")
    print(f"Потерянных : {model.lost_requests}", end=" ")
    print(f"Вероятность отказа: {round(model.getRejectProbability(), 3)}", end=" ")
    print(f"Коэффициент загрузки: {round(model.channel_busy_time / 1000, 3)}")

plt.plot(lambda_values, experiment_result, marker='o', label="Экспериментальные данные")
plt.plot(lambda_values, theory_result, marker='o', label="Теоретические данные (по формуле Эрланга)")
plt.xticks([i for i in range(10, 3 * mu_value + 1, 5)])
plt.title("Вероятность отказа от интенсивности входящего потока")
plt.ylabel("Вероятность отказа")
plt.xlabel("Интенсивность входящего потока (заявок в час)")
plt.legend()
plt.grid()
plt.show()
