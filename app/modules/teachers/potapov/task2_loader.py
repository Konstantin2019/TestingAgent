from random import gauss, randint, uniform, choice

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
    def __inner_gen__():
        pass

def __rk2_task3_gen():
    def __inner_gen__():
        pass

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