from random import randint


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

print(__rk2_task1_gen())