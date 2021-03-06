from json import loads, dumps
import re

class RK1_Checker():
    def __init__(self, correct_answer, answer):
        self.correct_answer = correct_answer
        self.answer = answer

    def __call__(self, index):
        try:
            correct_answer = loads(self.correct_answer)
            self.answer = self.answer.replace(',', '.').strip()
            spam = re.split('; |: |/ |;|:| |/|&', self.answer)
            if index == 1:
                if len(spam) != 2:
                    return 0, self.answer
                student_answer = { 'RE': float(spam[0]), 'SE': float(spam[1]) }
                RE_dif = (correct_answer['RE'] - student_answer['RE']) / correct_answer['RE']
                SE_dif = (correct_answer['SE'] - student_answer['SE']) / correct_answer['SE']
                if abs(RE_dif) <= 0.05 and abs(SE_dif) <= 0.05:
                    return 1, dumps(student_answer)
                else: 
                    return 0, dumps(student_answer)
            elif index == 2:
                if len(spam) != 1:
                    return 0, self.answer
                student_answer = { 'dF': float(spam[0]) }
                dF_dif = (correct_answer['dF'] - student_answer['dF']) / correct_answer['dF']
                if abs(dF_dif) <= 0.05:
                    return 1, dumps(student_answer)
                else:
                    return 0, dumps(student_answer)
            elif index == 3:
                if len(spam) != 2:
                    return 0, self.answer
                if correct_answer['k1'] < correct_answer['k2']:
                    student_answer = { 'k1': float(spam[0]), 'k2': float(spam[1]) } \
                                     if float(spam[0]) < float(spam[1]) \
                                     else { 'k2': float(spam[0]), 'k1': float(spam[1]) }
                elif correct_answer['k2'] < correct_answer['k1']:
                    student_answer = { 'k2': float(spam[0]), 'k1': float(spam[1]) } \
                                     if float(spam[0]) < float(spam[1]) \
                                     else { 'k1': float(spam[0]), 'k2': float(spam[1]) }
                else:
                    student_answer = { 'k1': float(spam[0]), 'k2': float(spam[1]) }
                k1_dif = (correct_answer['k1'] - student_answer['k1']) / correct_answer['k1']
                k2_dif = (correct_answer['k2'] - student_answer['k2']) / correct_answer['k2']
                if abs(k1_dif) <= 0.05 and abs(k2_dif) <= 0.05:
                    return 1, dumps(student_answer)
                else: 
                    return 0, dumps(student_answer)
            elif index == 4:
                if len(spam) != 2:
                    return 0, self.answer
                student_answer = { 'Ps': int(spam[0]), 'Pn': int(spam[1]) }
                Ps_dif = (correct_answer['Ps'] - student_answer['Ps']) / correct_answer['Ps']
                Pn_dif = (correct_answer['Pn'] - student_answer['Pn']) / correct_answer['Pn']
                if abs(Ps_dif) <= 0.05 and abs(Pn_dif) <= 0.05:
                    return 1, dumps(student_answer)
                else: 
                    return 0, dumps(student_answer)
            elif index == 5:
                if len(spam) != 1:
                    return 0, self.answer
                student_answer = { 'delta_instr': float(spam[0]) }
                delta_instr_dif = (correct_answer['delta_instr'] - student_answer['delta_instr']) / correct_answer['delta_instr']
                if abs(delta_instr_dif) <= 0.05:
                    return 1, dumps(student_answer)
                else:
                    return 0, dumps(student_answer)
        except Exception:
            return 0, self.answer

class RK2_Checker():
    def __init__(self, correct_answer, answer):
        self.correct_answer = correct_answer
        self.answer = answer

    def __call__(self, index):
        try:
            correct_answer = loads(self.correct_answer)
            self.answer = self.answer.replace(',', '.').strip()
            spam = re.split('/ | |/', self.answer)
            if index == 1:
                if len(spam) < 1 and len(spam) > 2:
                    return 0, self.answer
                student_answer = { 'valid': spam[0], \
                                   'explanation': spam[1] if len(spam) == 2 else '??????' }
                if student_answer['valid'] == correct_answer['valid']:
                    return 1, dumps(student_answer, ensure_ascii=False)
                else: 
                    return 0, dumps(student_answer, ensure_ascii=False)
            elif index == 2:
                if len(spam) < 3 and len(spam) > 4:
                    return 0, self.answer
                student_answer = { 'valid': [spam[0], spam[1], spam[2]], \
                                   'explanation': spam[3] if len(spam) == 4 else '??????' }
                score = 0
                for k in range(3):
                    if student_answer['valid'][k] == correct_answer['valid'][k]:
                        score += 1
                if score == 3:
                    return 1, dumps(student_answer, ensure_ascii=False)
                else:
                    return 0, dumps(student_answer, ensure_ascii=False)
            elif index == 3:
                if len(spam) < 1 and len(spam) > 2:
                    return 0, self.answer
                student_answer = { 'valid': spam[0], \
                                   'explanation': spam[1] if len(spam) == 2 else '??????' }
                if student_answer['valid'] == correct_answer['valid']:
                    return 1, dumps(student_answer, ensure_ascii=False)
                else: 
                    return 0, dumps(student_answer, ensure_ascii=False) 
            elif index == 4:
                if len(spam) != 2:
                    return 0, self.answer
                student_answer = { 'Rkmin': float(spam[0]), 'Rkmax': float(spam[1]) }
                Rkmin_dif = (correct_answer['Rkmin'] - student_answer['Rkmin']) / correct_answer['Rkmin']
                Rkmax_dif = (correct_answer['Rkmax'] - student_answer['Rkmax']) / correct_answer['Rkmax']
                if abs(Rkmin_dif) <= 0.05 and abs(Rkmax_dif) <= 0.05:
                    return 2, dumps(student_answer)
                else: 
                    return 0, dumps(student_answer)
        except Exception:
            return 0, self.answer
    