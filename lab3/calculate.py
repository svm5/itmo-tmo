from task import run_modeling
from calculate_theory import calculate_theory

lamd = 3
mu = 4
m = 6
modeling_time = 2000
a = run_modeling(lamd, mu, m, modeling_time)
b = calculate_theory(lamd, mu, m)
print("Теория")
for key, val in a.items():
    print(key, val)
print("Модель")
for key, val in b.items():
    print(key, val)
