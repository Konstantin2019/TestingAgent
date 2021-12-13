from app import app, sql_provider, store
from app.models.shemas import Student
from time import sleep

def do_on_complete(student_id, test_name, job_name):
    student = sql_provider.get(Student, student_id)
    remaining_time = student.rk1_remaining_time if test_name == 'rk1' \
                     else student.rk2_remaining_time
    if remaining_time == 0:
        sleep(60)
        patch = {'rk1_status': 'Done'} if test_name == 'rk1' else {'rk2_status': 'Done'}
        sql_provider.update(Student, student_id, patch)
        print(f'Планировщик с именем {job_name} завершил работу')
        app.apscheduler.remove_job(job_name)
    else:
        patch = {'rk1_remaining_time': remaining_time - store['interval']} if test_name == 'rk1' \
               else {'rk2_remaining_time': remaining_time - store['interval']}
        sql_provider.update(Student, student_id, patch)
