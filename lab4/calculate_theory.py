def calculate_theory(lambda1, lambda2, mu):
    rho1 = lambda1 / mu
    rho2 = lambda2 / mu
    w1 = rho1 / (mu * (1 - rho1))
    t1 = w1 + 1 / mu
    w2 = (lambda1 + lambda2) / (mu ** 2 * (1 - rho1) * (1 - rho1 - rho2))
    t2 = w2 + 1 / mu
    p1 = rho1
    p2 = rho1 + rho2
    rho = rho1 + rho2
    system_avg = lambda1 * t1 + lambda2 * t2
    
    return {
        "w1":  w1,
        "w2": w2,
        "t1": t1,
        "t2":  t2,
        "p1":  p1,
        "p2":  p2,
        "rho": rho,
        "avg": system_avg
    }

