from random import randint, uniform, choice
from math import sqrt
from json import load, dumps

#region inner_gen_funcs
def __rk2_task1_gen():
    def __inner_gen__(D, EsD, EiD, S, EsS, EiS):
        d = D - 2*S
        Esd = EsD - 2*EsS
        Eid = EiD - 2*EiS
        return {'Task': {'D': D, 'EsD': EsD, 'EiD': EiD, 'S': S, 'EsS': EsS, 'EiS': EiS}, \
                'Answer': {'d': d, 'Esd': Esd, 'Eid': Eid}}
    D = randint(20, 100)
    EsD = randint(0, 300)
    TD = randint(300, 600)
    S = randint(0,2)
    EsS = randint(-100, 100)
    TS = randint(30, 90)
    return __inner_gen__(D=D, EsD=EsD, EiD=EsD-TD, S=S, EsS=EsS, EiS=EsS-TS)

def __rk2_task2_gen():
    pass
  

def __rk2_task3_gen():
    pass
  
#endregion

#region inner_prepare_funcs
def __rk2_task1_prepare(text, values):
    pass
    
def __rk2_task2_prepare(text, values):
    pass

def __rk2_task3_prepare(text, values):
    pass

#endregion

def load_tasks(filepath):
    try:
        with open(filepath, encoding='utf-8', mode='r') as fp:
            rk2_tasks = load(fp) 
        rk2_task1_text = rk2_tasks['Задание №1']
        rk2_task2_text = rk2_tasks['Задание №2']
        rk2_task3_text = rk2_tasks['Задание №3']

        rk2_task1_values = __rk2_task1_gen()
        rk2_task2_values = __rk2_task2_gen()
        rk2_task3_values = __rk2_task3_gen()

        result = {}
        rk2_task1 = __rk2_task1_prepare(rk2_task1_text, rk2_task1_values)
        result.update(rk2_task1)
        rk2_task2 = __rk2_task2_prepare(rk2_task2_text, rk2_task2_values)
        result.update(rk2_task2)
        rk2_task3 = __rk2_task3_prepare(rk2_task3_text, rk2_task3_values)
        result.update(rk2_task3)

        return result
    except Exception as error:
        return error