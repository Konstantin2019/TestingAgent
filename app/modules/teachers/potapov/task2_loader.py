from random import gauss, randint, uniform, choice
from collections import namedtuple
from numpy import mean, std

#region inner_gen_funcs
def __rk2_task1_gen():
    def __inner_calculator__(d, P):
        H = 0.866025*P
        d2 = d - 2*(3/8)*H
        d1 = d - 2*(5/8)*H
        return d2, d1
    def __inner_gen__(d, P, T, dr, d2r, d1r, fp, fa):
        valid = ''
        thread_type = choice(['гайка', 'болт'])
        d2, d1 = __inner_calculator__(d, P)
        if thread_type == 'болт':
            dmax, dmin = d, d - T
            d2max, d2min = d2, d2 - T
            d1max = d1
            if dmin <= dr <= dmax and \
               d2r >= d2min and \
               d2r + fp + fa <= d2max and \
               d1r <= d1max:
               valid = 'годно'
            else:
               valid = 'брак'
        else:
            D, D2, D1 = d, d2, d1
            Dr, D2r, D1r = dr, d2r, d1r
            Dmin = D
            D2max, D2min = D2 + T, D2 
            D1max, D1min = D1 + T, D1
            if D1min <= D1r <= D1max and \
               D2r <= D2max and \
               D2r - fp - fa >= D2min and \
               Dr >= Dmin:
               valid = 'годно'
            else:
               valid = 'брак'
        return {'Task': {'type': thread_type, 'd': d, 'd2': d2, 'd1': d1, \
                'dr': dr, 'd2r': d2r, 'd1r': d1r, 'fp': fp, 'fa': fa}, \
                'Answer': {'valid': valid}}
    d = randint(20, 60)
    P = randint(1,4)
    d2, d1 = __inner_calculator__(d, P)
    T = uniform(0.02, 0.1)
    return __inner_gen__(d=d, P=P, T=T, \
                         dr=d+uniform(-T/2, T/2), d2r=d2+uniform(-T/2, T/2), \
                         d1r=d1+uniform(-T/2, T/2), fp=uniform(0.005, 0.02), \
                         fa=uniform(0.005, 0.02) )    

def __rk2_task2_gen():
    F = {'8': 80, '7': 70, '6': 60}
    f = {'8': 40, '7': 30, '6': 20}
    controlled_gear = namedtuple('gear', 'Fr fr')
    def __inner_gear_gen__():
        t = randint(6,8)
        p = randint(6,8)
        k = randint(6,8)
        jnmin = ['A','B','C','D','E','H']
        Tjn = ['a','b','c','d','e','h']
        if t == p and t == k:
            return str(t)+choice(jnmin)+choice(Tjn)
        else:
            return str(t)+"-"+str(p)+"-"+str(k)+choice(jnmin)+choice(Tjn)
    def __inner_gear_parse__(gear):
        if len(gear) > 3:
            t = gear[0]
            p = gear[2]
            k = gear[4]
            jnmin = gear[5]
            Tjn = gear[6]
        else:
            t = gear[0]
            p = t
            k = t
            jnmin = gear[1]
            Tjn = gear[2]
        return {'t': t, 'p': p, 'k': k, 'jnmin': jnmin, 'Tjn': Tjn}
    def __inner_task_gen__():
        gear = __inner_gear_gen__()
        gears = [controlled_gear(Fr=randint(55, 85), fr=randint(15, 45)) for i in range(3)]
        parsed_gear = __inner_gear_parse__(gear)
        returned_dict = {'Task': {'accuracy': gear, 'F': F, 'f': f, 'gears': gears}, 'Answer': {'valid': []}}
        for g in gears:
            if g.Fr <= F[parsed_gear['t']] and g.fr <= f[parsed_gear['k']]:
                returned_dict['Answer']['valid'].append('годно')
            else:
                returned_dict['Answer']['valid'].append('брак')
        return returned_dict
    return __inner_task_gen__()
        
def __rk2_task3_gen():
    def __inner_gen__(mu, sigma, delta, T, n):
        operand = choice(['+', '-'])
        if operand == '+':
            X = [gauss(mu, sigma) + delta for i in range(n)]
        if operand == '-':
            X = [gauss(mu, sigma) - delta for i in range(n)]
        P = choice([0.95, 0.99])
        if P == 0.95:
            k = 2
        else:
            k = 3
        Xmin = mu - T/2
        Xmax = mu + T/2
        Xqmin = mean(X) - k*std(X, ddof=1)
        Xqmax = mean(X) + k*std(X, ddof=1)
        returned_dict = {'Task': {'X': X, 'P': P, 'n': n}, 'Answer': {'valid': ''}}
        if Xqmin >= Xmin and Xqmax <= Xmax:
            returned_dict['Answer']['valid'] = 'годно'
        else:
            returned_dict['Answer']['valid'] = 'брак'
    mu = randint(10,100)
    T = uniform(0.03,0.1)
    sigma = T/choice([4,5,6])
    delta = uniform(0.002,0.01)
    return __inner_gen__(mu=mu, sigma=sigma, delta=delta, T=T, n=randint(30,50))

def __rk2_task4_gen():
    def __inner_gen__():
        pass
#endregion

#region inner_prepare_funcs
def __rk2_task1_prepare(text, values):
    pass
    
def __rk2_task2_prepare(text, values):
    pass

def __rk2_task3_prepare(text, values):
    pass

def __rk2_task4_prepare(text, values):
    pass
#endregion

def load_tasks(filepath):
    pass