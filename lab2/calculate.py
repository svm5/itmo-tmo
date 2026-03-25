from task import PassengerBoardingModel

from math import factorial

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
fixed_channels_count = 4
model = PassengerBoardingModel(fixed_lambda, fixed_mu_value, fixed_channels_count, 2000)
model.run()
print("Вероятность простоя системы (все каналы свободны) (модель - теория):")
print(model.system.calculateDowntimeProbability(), calculateDowntimeProbability(fixed_lambda, fixed_mu_value, fixed_channels_count))
print("Вероятность того, что заявка будет ждать в очереди (модель - теория):")
print(model.system.queueWaitProbability(), queueWaitProbability(fixed_lambda, fixed_mu_value, fixed_channels_count))
print("Среднее число заявок в очереди (модель - теория)")
print(model.system.calculateAverageRequestsInQueueCount(), calculateAverageRequestsInQueueCount(fixed_lambda, fixed_mu_value, fixed_channels_count))
print("Среднее время ожидания заявки в очереди (модель - теория)")
print(model.system.calculateAverageRequestInQueueTime(), calculateAverageRequestInQueueTime(fixed_lambda, fixed_mu_value, fixed_channels_count))
print("Среднее время пребывания заявки в системе (модель - теория)")
print(model.system.calculateAverageRequestTime(), calculateAverageRequestTime(fixed_lambda, fixed_mu_value, fixed_channels_count))
print("Коэффициент загрузки системы (модель - теория)")
print(model.system.calculateLoadCoefficient(), calculateLoadCoefficient(fixed_lambda, fixed_mu_value, fixed_channels_count))
