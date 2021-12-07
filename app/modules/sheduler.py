from app import app, sql_provider, store
from app.models.shemas import Student, RK1, RK2
from time import sleep

def do_on_complete(student_id, test_name, job_name):
    def __finallize():
        total_score = 0
        try:
            rk_objs = sql_provider.query(RK1).filter_by(student_id=student_id).all() \
                     if test_name == 'rk1' else sql_provider.query(RK2).filter_by(student_id=student_id).all()
            rk_scores = [item.score if item else 0 for item in rk_objs]
            total_score = sum(rk_scores)
            patch = {'rk1_status': 'Done', 'rk1_score': total_score} \
                    if test_name == 'rk1' else {'rk2_status': 'Done', 'rk2_score': total_score}
            sql_provider.update(Student, student_id, patch)
        except Exception as err:
            total_score = 0
            print(err)
        finally:
            print(f'Планировщик с именем {job_name} завершил работу')
            app.apscheduler.remove_job(job_name)
    student = sql_provider.get(Student, student_id)
    remaining_time = student.rk1_remaining_time if test_name == 'rk1' \
                     else student.rk2_remaining_time
    if remaining_time == 0:
        sleep(60)
        __finallize()
    else:
        patch = {'rk1_remaining_time': remaining_time - store['interval']} if test_name == 'rk1' \
               else {'rk2_remaining_time': remaining_time - store['interval']}
        sql_provider.update(Student, student_id, patch)
