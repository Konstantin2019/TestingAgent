from random import gauss, randint, uniform, choice
from collections import namedtuple
from numpy import mean, std

#region inner_gen_funcs
def __rk2_task1_gen():
    def __inner_calculator__(d, P):
        H = 0.866025*P
        d2 = round(d - 2*(3/8)*H, 3)
        d1 = round(d - 2*(5/8)*H, 3)
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
                'Answer': {'valid': valid}
               }
    d = randint(20, 60)
    P = randint(1,4)
    d2, d1 = __inner_calculator__(d, P)
    T = round(uniform(0.02, 0.1), 3)
    return __inner_gen__(d=d, P=P, T=T, \
                         dr=d+round(uniform(-T/2, T/2), 3), d2r=d2+round(uniform(-T/2, T/2), 3), \
                         d1r=d1+round(uniform(-T/2, T/2), 3),
                         fp=round(uniform(0.005, 0.02), 3), fa=round(uniform(0.005, 0.02), 3))    

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
        returned_dict = {'Task': {'accuracy': gear, 'F': F, 'f': f, \
                         'gear1': (f'Fr={gears[0].Fr}', f'fr={gears[0].fr}'), \
                         'gear2': (f'Fr={gears[1].Fr}', f'fr={gears[1].fr}'), \
                         'gear3': (f'Fr={gears[2].Fr}', f'fr={gears[2].fr}'), \
                         'Answer': {'valid': []}}
                        }
        for g in gears:
            if g.Fr <= F[parsed_gear['t']] and g.fr <= f[parsed_gear['k']]:
                returned_dict['Answer']['valid'].append('годно')
            else:
                returned_dict['Answer']['valid'].append('брак')
        return returned_dict
    return __inner_task_gen__()
        
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
        Xmin = mu - T/2
        Xmax = mu + T/2
        Xqmin = mean(X) - k*std(X, ddof=1)
        Xqmax = mean(X) + k*std(X, ddof=1)
        if Xqmin >= Xmin and Xqmax <= Xmax:
            valid = 'годно'
        else:
            valid = 'брак'
        return {'Task': {'X': X, 'P': P, 'n': n}, 'Answer': {'valid': valid}}
    mu = randint(10,100)
    T = uniform(0.03,0.1)
    sigma = T/choice([4,5,6])
    delta = uniform(0.002,0.01)
    return __inner_gen__(mu=mu, sigma=sigma, delta=delta, T=T, n=randint(30,50))

def __rk2_task4_gen():
    def __inner_gen__(R, EsR, EiR):
        R1, R2, R3, Rs = R
        EsR1, EsR2, EsR3, EsRs = EsR
        EiR1, EiR2, EiR3, EiRs = EiR
        EmR1 = (EsR1+EiR1)/2
        EmR2 = (EsR2+EiR2)/2
        EmR3 = (EsR3+EiR3)/2
        EmRs = (EsRs+EiRs)/2
        TR1 = EsR1 - EiR1
        TR2 = EsR2 - EiR2
        TR3 = EsR3 - EiR3
        TRs = EsRs - EiRs
        R23 = R2*R3/(R2+R3)
        if (EmR2+EmR3) != 0:
            EmR23 = EmR2*EmR3/(EmR2+EmR3)
        else:
            EmR23 = 0
        TR23 = (R3/(R2+R3)-R2*R3/(R2+R3)**2)*TR2 + (R2/(R2+R3)-R2*R3/(R2+R3)**2)*TR3   
        Rk = Rs - (R1 + R23)
        Vk = TR1 + TR23 - TRs
        EmRk = EmRs-EmR1-EmR23
        EsRk = EmRk + Vk/2
        EiRk = EmRk - Vk/2
        Rkmin = Rk + EiRk
        Rkmax = Rk + EsRk
        return {'Task': {'R1': R[0], 'R2': R[1], 'R3': R[2], 'Rs': R[3], \
                         'EsR1': EsR[0], 'EsR2': EsR[1], 'EsR3': EsR[2], 'EsRs': EsR[3], \
                         'EiR1': EiR[0], 'EiR2': EiR[1], 'EiR3': EiR[2], 'EiRs': EiR[3]}, \
                'Answer': {'Rkmin': round(Rkmin, 1), 'Rkmax': round(Rkmax, 1)}
               }
    return __inner_gen__([randint(200,250), randint(200,250), randint(200,250), randint(400,500)], \
                         [round(uniform(1,2), 1), round(uniform(1,2), 1), \
                          round(uniform(1,2), 1), round(uniform(1,2), 1)], \
                         [round(uniform(-2,-1), 1), round(uniform(-2,-1), 1), \
                          round(uniform(-2,-1), 1), round(uniform(-2,-1), 1)])
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