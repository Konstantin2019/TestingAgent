
from random import choice, gauss, randint, uniform
from numpy import mean, std

def __rk2_task3_gen():
    def __inner_gen__(mu, sigma, delta, T, n):
        valid = ''
        operand = choice(['+', '-'])
        if operand == '+':
            X = [round(gauss(mu, sigma) + delta, 3) for i in range(n)]
        if operand == '-':
            X = [round(gauss(mu, sigma) - delta, 3) for i in range(n)]
        P = choice([0.95, 0.99])
        if P == 0.95:
            k = 2
        else:
            k = 3
        Xmin = round(mu - T/2, 3)
        Xmax = round(mu + T/2, 3)
        Xqmin = round(mean(X) - k*std(X, ddof=1), 3)
        Xqmax = round(mean(X) + k*std(X, ddof=1), 3)
        if Xqmin >= Xmin and Xqmax <= Xmax:
            valid = 'годно'
        else:
            valid = 'брак'
        return {'Task': {'X': X, 'P': P, 'n': n, 'Xmin': Xmin, 'Xmax': Xmax}, \
                'Answer': {'valid': valid}
               }
    mu = randint(10,100)
    T = uniform(0.03,0.1)
    sigma = T/choice([4,5,6])
    delta = uniform(0.002,0.01)
    return __inner_gen__(mu=mu, sigma=sigma, delta=delta, T=T, n=randint(30,50))

print(__rk2_task3_gen())