from json import loads, dumps
import re

class RK1_Checker():
    def __init__(self, correct_answer, answer):
        self.correct_answer = correct_answer
        self.answer = answer

    def __call__(self, index):
        try:
            correct_answer = loads(self.correct_answer)
            self.answer = self.answer.replace(',', '.')
            spam = re.split('; |: |;|:| |/|&', self.answer)
            if index == 1:
                if len(spam) != 2:
                    return 0, self.answer
                student_answer = { 'RE': float(spam[0]), 'SE': float(spam[1]) }
                RE_dif = (correct_answer['RE'] - student_answer['RE']) / correct_answer['RE']
                SE_dif = (correct_answer['RE'] - student_answer['RE']) / correct_answer['RE']
                if abs(RE_dif) < 0.05 and abs(SE_dif) < 0.05:
                    return 12, dumps(student_answer)
                else: 
                    return 0, dumps(student_answer)
            elif index == 2:
                if len(spam) != 4:
                    return 0, self.answer
                student_answer = { 'Smax': int(spam[0]), 'Smin': int(spam[1]), \
                                   'Sm': int(spam[2]), 'Ts': int(spam[3]) }
                Smax_dif = (correct_answer['Smax'] - student_answer['Smax']) / correct_answer['Smax']
                Smin_dif = (correct_answer['Smin'] - student_answer['Smin']) / correct_answer['Smin']
                Sm_dif = (correct_answer['Sm'] - student_answer['Sm']) / correct_answer['Sm']
                Ts_dif = (correct_answer['Ts'] - student_answer['Ts']) / correct_answer['Ts']
                if abs(Smax_dif) < 0.05 and abs(Smin_dif) < 0.05 \
                   and abs(Sm_dif) < 0.05 and abs(Ts_dif) < 0.05:
                    return 12, dumps(student_answer)
                else:
                    return 0, dumps(student_answer)
            elif index == 3:
                if len(spam) != 2:
                    return 0, self.answer
                student_answer = { 'k1': float(spam[0]), 'k2': float(spam[1]) }
                k1_dif = (correct_answer['k1'] - student_answer['k1']) / correct_answer['k1']
                k2_dif = (correct_answer['k2'] - student_answer['k2']) / correct_answer['k2']
                if abs(k1_dif) < 0.05 and abs(k2_dif) < 0.05 and student_answer['k1'] < student_answer['k2']:
                    return 12, dumps(student_answer)
                else: 
                    return 0, dumps(student_answer)
            elif index == 4:
                if len(spam) != 4:
                    return 0, self.answer
                student_answer = { 'Nmax': int(spam[0]), 'Nmin': int(spam[1]), \
                                   'Nm': int(spam[2]), 'Tn': int(spam[3]) }
                Nmax_dif = (correct_answer['Nmax'] - student_answer['Nmax']) / correct_answer['Nmax']
                Nmin_dif = (correct_answer['Nmin'] - student_answer['Nmin']) / correct_answer['Nmin']
                Nm_dif = (correct_answer['Nm'] - student_answer['Nm']) / correct_answer['Nm']
                Tn_dif = (correct_answer['Tn'] - student_answer['Tn']) / correct_answer['Tn']
                if abs(Nmax_dif) < 0.05 and abs(Nmin_dif) < 0.05 \
                   and abs(Nm_dif) < 0.05 and abs(Tn_dif) < 0.05:
                    return 12, dumps(student_answer)
                else:
                    return 0, dumps(student_answer)
            elif index == 5:
                if len(spam) != 1:
                    return 0, self.answer
                student_answer = { 'delta_instr': float(spam[0]) }
                delta_instr_dif = (correct_answer['delta_instr'] - student_answer['delta_instr']) / correct_answer['delta_instr']
                if abs(delta_instr_dif) < 0.05:
                    return 12, dumps(student_answer)
                else:
                    return 0, dumps(student_answer)
        except Exception:
            return 0, self.answer

class RK2_Checker():
    pass