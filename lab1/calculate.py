from task import PassengerBoardingModel

lambda_value = 2000
mu_value = 6
time_value = 1000

model = PassengerBoardingModel(lambda_value, mu_value, time_value)
model.run()
print(f"Количество поступивших заявок: {model.incoming_requests}")
print(f"Количество обсуженных заявок: {model.served_requests}")
print(f"Количество потерянных заявок: {model.lost_requests}")
print(f"Вероятность отказа (доля потерянных заявок): {round(model.getRejectProbability(), 3)}")
print(f"Коэффициент загрузки системы (доля времени, когда канал занят): {round(model.channel_busy_time / time_value, 3)}")
