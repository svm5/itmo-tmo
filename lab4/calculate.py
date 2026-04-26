from calculate_theory import calculate_theory
from task import start_model

lambda1 = 5
lambda2 = 30
mu = 60
a = start_model(lambda1, lambda2, mu, 10000, 0)
b = calculate_theory(lambda1, lambda2, mu)

print("Модель - Теория")
print("Среднее время ожидания в очереди высокоприоритетных заявок", round(a["w1"], 5), round(b["w1"], 5), sep="\t")
print("Среднее время ожидания в очереди низкоприоритетных заявок", round(a["w2"], 5), round(b["w2"], 5), sep="\t")
print("Среднее время пребывания в системе высокоприоритетных заявок", round(a["t1"], 5), round(b["t1"], 5), sep="\t")
print("Среднее время пребывания в системе низкоприоритетных заявок", round(a["t2"], 5), round(b["t2"], 5), sep="\t")
print("Вероятность того, что высокоприоритеная заявка будет ждать в очереди", round(a["p1"], 5), round(b["p1"], 5), sep="\t")
print("Вероятность того, что низкоприоритетная заявка будет ждать в очереди", round(a["p2"], 5), round(b["p2"], 5), sep="\t")
print("Коэффициент загрузки системы", round(a["rho"], 5), round(b["rho"], 5), sep="\t")
print("Среднее число заявок в системе", round(a["avg"], 5), round(b["avg"], 5), sep="\t")
# for key, val in a.items():
#     print(key, round(val, 5))

# print("Теория")
# for key, val in b.items():
#     print(key, round(val, 5))

# print(a["high"])
# print(a["low"])
# print(a["system"])
# for key, val in a["high"].items():
#     print(key, round(val, 3))
# for key, val in a["low"].items():
#     print(key, round(val, 3))
# for key, val in a["system"].items():
#     print(key, round(val, 3))
# print("Модель")
# print(a)
# for key, val in a.items():
#     print(key, round(val, 5))