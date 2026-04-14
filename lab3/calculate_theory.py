def calculate_theory(lamd, mu, m):
    rho = lamd / mu

    p_0 = (1 - rho) / (1 - rho ** (m + 2))
    p_loss = rho ** (m + 1) * p_0
    l_s = 0
    for k in range(m + 2):
        l_s += k * rho ** k * p_0
    l_q = l_s - (1 - p_0)
    lambda_e = lamd * (1 - p_loss)

    w_q = l_q / lambda_e
    w_s = l_s / lambda_e

    return {
        "Вероятность потери заявок": p_loss,
        "Среднее число заявок в очереди": l_q,
        "Среднее время ожидания заявки в очереди": w_q,
        "Среднее время пребывания заявки в системе": w_s,
        "Коэффициент загрузки системы": lamd / mu,
        "lambda_eff": lambda_e / mu
    }