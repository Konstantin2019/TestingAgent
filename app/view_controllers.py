from hashlib import sha1
import json
from flask import render_template, request, redirect, jsonify
from flask.helpers import flash, make_response, url_for
from datetime import datetime
from app.modules.sheduler import do_on_complete
from app.models.shemas import Group, Student, Year, RK1, RK2
from app.models.view_models import StudentAuth, AdminAuth
from app import sql_provider, store
from app.modules.task_selector import select

def init_controllers(app):
    @app.route('/error')
    def error():
        return render_template('error.html')
    #region Student
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/auth', methods=['GET', 'POST'])
    def auth():
        auth_view = StudentAuth()
        current_year = datetime.now().year
        if request.method == "GET":
            year_record = sql_provider.query(Year).filter_by(year_name=current_year).scalar()
            if year_record:
                groups = [group.group_name for group in year_record.groups if group.year_id == year_record.id]
                auth_view.group.choices = groups
                store['groups'] = groups
            else:
                auth_view.group.choices = []
            return render_template('auth_form.html', form=auth_view)
        if auth_view.validate_on_submit():
            year_record = sql_provider.query(Year).filter_by(year_name=current_year).scalar()
            if auth_view.group.data:
                group = Group(group_name=auth_view.group.data, year_id=year_record.id)
                group_id = sql_provider.set(group)
                student = Student(surname=auth_view.surname.data, name=auth_view.name.data, \
                                  patronymic=auth_view.patronymic.data, group_id=group_id, \
                                  rk1_status='Ready', rk1_remaining_time=store['time_for_rk1'], rk1_score=0, \
                                  rk2_status='Ready', rk2_remaining_time=store['time_for_rk2'], rk2_score=0)
                student_id = sql_provider.set(student)
                rk_choice = auth_view.test.data
                return redirect(url_for('test', student_id=student_id, rk_choice=rk_choice, teacher=auth_view.teacher.data))
            else:
                return redirect(url_for('index'))
        else:
            auth_view.group.choices = store['groups']
            return render_template('auth_form.html', form=auth_view)

    @app.route('/test/<int:student_id>/<string:rk_choice>/<string:teacher>', methods=['GET', 'POST'])
    def test(student_id: int, rk_choice: str, teacher: str):
        test_name = rk_choice.lower()
        checker, task1_loader, task2_loader = select(teacher)
        sheduler_id = f'{test_name}_{student_id}_{teacher}'
        if request.method == 'GET':
            student = sql_provider.get(Student, student_id)
            if request.args.get('remaining_time'):
                remaining_time = student.rk1_remaining_time if test_name == 'rk1' \
                                 else student.rk2_remaining_time
                return make_response(json.dumps(remaining_time), 200)
            interval = store['interval']
            if test_name == 'rk1':
                if (student.rk1_status == 'Done'):
                    return redirect(url_for('error'))
                if (student.rk1_status != 'Started'):
                    try:
                        rk1 = task1_loader.load_tasks(f'app/static/files/{teacher}/rk1.json')
                        rk1_obj_list = [RK1(question=text, correct_answer=answer, student_id=student_id, score=0)
                                        for text, answer in rk1.items()]
                        sql_provider.set_many(rk1_obj_list)
                        sql_provider.update(Student, student_id, {'rk1_status': 'Started'})
                        app.apscheduler.add_job(func=do_on_complete, trigger='interval', minutes=interval, \
                                                args=[student_id, test_name, sheduler_id], id=sheduler_id)
                        print(f'Планировщик с именем {sheduler_id} начал работу...')
                    except Exception:
                        return make_response('<h1>Ошибка загрузки РК№2</h1>', 404)
                else:
                    rk1_obj_list = sql_provider.query(RK1).filter_by(student_id=student_id).all()
                questions = [obj.question for obj in rk1_obj_list]
                return render_template('test.html', surname=student.surname, type='РК№1', questions=enumerate(questions))
            elif test_name == 'rk2':
                if (student.rk2_status == 'Done'):
                    return redirect('error.html')
                if (student.rk1_status != 'Started'):
                    try:
                        rk2 = task2_loader.load_tasks(f'app/static/files/{teacher}/rk2.json')
                        rk2_obj_list = [RK2(question=text, correct_answer=answer, student_id=student_id, score=0)
                                    for text, answer in rk2.items()]
                        sql_provider.set_many(rk2_obj_list)
                        sql_provider.update(Student, student_id, {'rk2_status': 'Started'})
                        app.apscheduler.add_job(func=do_on_complete, trigger='interval', minutes=interval, \
                                                args=[student_id, test_name, sheduler_id], id=sheduler_id)
                        print(f'Планировщик с именем {sheduler_id} начал работу...')
                    except Exception:
                        return make_response('<h1>Ошибка загрузки РК№2</h1>', 404)
                else:
                    rk2_obj_list = sql_provider.query(RK2).filter_by(student_id=student_id).all()
                questions = [obj.question for obj in rk2_obj_list]
                return render_template('test.html', surname=student.surname, type='РК№2', questions=rk2)
            else:
                return make_response('<h1>Что-то не так с запросом:(</h1>', 404)
        if request.method == 'POST':
            try:
                data = request.get_json()
                student = sql_provider.get(Student, student_id)
                rk_status = student.rk1_status if test_name == 'rk1' else student.rk2_status
                if rk_status == 'Done':
                    return make_response(jsonify('Время на выполнение истекло!'), 503)
                if 'status' in data and data['status'] == 'finish':
                    do_on_complete(student_id, test_name, sheduler_id)
                    return make_response('', 200)
                if 'student_answer' in data and data['student_answer']:
                    student_answer = data['student_answer']
                    test_cls = RK1 if test_name == 'rk1' else RK2
                    question_id = sql_provider.query(test_cls).filter_by(question=data['question']).scalar().id
                    if question_id:
                        correct_answer = sql_provider.get(test_cls, question_id).correct_answer
                        score, student_answer = checker.RK1_Checker(correct_answer, student_answer)(int(data['index'])) \
                                                if test_name == 'rk1' \
                                                else checker.RK2_Checker(correct_answer, student_answer)(int(data['index']))
                        sql_provider.update(test_cls, question_id, {'student_answer': student_answer})
                        sql_provider.update(test_cls, question_id, {'score': score})
                        return make_response('', 201)
                    else:
                        return make_response(json.dumps('Ошибка поиска в БД: id вопроса не найден!'), 500)
                else:
                    return make_response(json.dumps('Ошибка запроса: ответ студента не найден!'), 400)
            except Exception as err:
                return make_response(json.dumps(err), 500)
    #endregion

    #region Admin
    @app.route('/admin_auth', methods=['GET', 'POST'])
    def admin_auth():
        auth_view = AdminAuth()
        if request.method == "GET":
            return render_template('admin_auth.html', form=auth_view)
        if request.method == "POST":
            input_hash_code = sha1(str.encode(auth_view.password.data)).hexdigest()
            correct_hash_code = sha1(str.encode(app.config['ADMIN_PASSWORD'])).hexdigest() 
            if auth_view.login.data == app.config['ADMIN_LOGIN'] and input_hash_code == correct_hash_code:
                admin_login = request.cookies.get('admin_login')
                admin_password = request.cookies.get('admin_password')
                if admin_login and admin_password:
                    return redirect(url_for('admin'))
                else:
                    response = redirect(url_for('admin'))
                    response.set_cookie('admin_login', auth_view.login.data)
                    response.set_cookie('admin_password', correct_hash_code)
                    return response
            else:
                flash("Неверная пара: логин/пароль")
                return render_template('admin_auth.html', form=auth_view)

    @app.route('/admin', methods=['GET', 'POST'])
    def admin():
        admin_login = request.cookies.get('admin_login')
        admin_password = request.cookies.get('admin_password')
        if not admin_login and not admin_password:
            return redirect(url_for('admin_auth'))
        correct_hash_code = sha1(str.encode(app.config['ADMIN_PASSWORD'])).hexdigest()
        if admin_login != app.config['ADMIN_LOGIN'] and admin_password != correct_hash_code:
            return redirect(url_for('admin_auth'))
        if request.method == "GET":
            if not request.args:
                years = sql_provider.get_all(Year)
                groups, students = [], []
                return render_template('admin.html', years=years, groups=groups, students=enumerate(students))
            year_id = request.args.get('year')
            group_id = request.args.get('group')
            student_id = request.args.get('student')
            method = request.args.get('method')
            rk = request.args.get('rk')
            if method and method == 'view':
                student = sql_provider.get(Student, student_id) if student_id else None
                if student:
                    if rk and rk == 'rk1':
                        rk1 = student.rk1_questions
                        jsonified_rk = [jsonify(id=question.id, question=question.question, student_answer=question.student_answer, \
                                        correct_answer=question.correct_answer, score=question.score) \
                                        .data.decode('utf-8') for question in rk1]
                    elif rk and rk == 'rk2':
                        rk2 = student.rk2_questions
                        jsonified_rk = [jsonify(id=question.id, question=question.question, student_answer=question.student_answer, \
                                        correct_answer=question.correct_answer, score=question.score) \
                                        .data.decode('utf-8') for question in rk2]
                    return make_response(json.dumps(jsonified_rk), 200)
            if year_id and not group_id:
                year = sql_provider.get(Year, year_id)
                groups = [group for group in year.groups if group.year_id == year.id]
                jsonfied_groups = [jsonify(id=group.id, group_name=group.group_name)\
                                   .data.decode('utf-8') for group in groups]
                return make_response(json.dumps(jsonfied_groups), 200)
            if year_id and group_id:
                group = sql_provider.get(Group, group_id)
                students = [student for student in group.students]
                jsonfied_students = [jsonify(id=student.id, surname=student.surname, name=student.name, patronymic=student.patronymic, \
                                     rk1_score=student.rk1_score, rk2_score=student.rk2_score) \
                                     .data.decode('utf-8') for student in students]
                return make_response(json.dumps(jsonfied_students), 200)              
        if request.method == "POST":
            try:
                data = request.get_json()
                if 'method' in data and data['method'] == 'delete':
                    if 'group_id' in data and data['group_id']:
                        group_id = sql_provider.delete(Group, data['group_id'])
                        return make_response(jsonify(group_id), 200)
                    if 'student_id' in data and data['student_id']:
                        student_id = sql_provider.delete(Student, data['student_id'])
                        return make_response(jsonify(student_id), 200)
                if 'method' in data and data['method'] == 'create':
                    if 'group_name' in data and data['group_name']:
                        current_year = datetime.now().year
                        year_record = sql_provider.query(Year).filter_by(year_name=current_year).scalar()
                        if year_record:
                            group_id = sql_provider.set(Group(group_name=data['group_name'], year_id=year_record.id))
                        else:
                            year = Year(year_name=current_year)
                            id = sql_provider.set(year)
                            group_id = sql_provider.set(Group(group_name=data['group_name'], year_id=id))
                        return make_response(jsonify(group_id), 201)
                else:
                    return make_response('', 400)
            except Exception as err:
                return make_response(err, 500)  
    #endregion 