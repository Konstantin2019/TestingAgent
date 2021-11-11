from app import db
from sqlalchemy.orm import backref, synonym

class Year(db.Model):
    __tablename__ = 'years'
    id = db.Column(db.Integer, primary_key=True)
    year_name = db.Column(db.Integer, nullable=False)
    unique = synonym('year_name')
    groups = db.relationship('Group', backref='year', lazy=True, \
                              cascade='all, delete', passive_deletes=True)

    def __repr__(self):
        return f'<year {self.year_name}>'

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(12), nullable=False)
    unique = synonym('group_name')
    year_id = db.Column(db.Integer, db.ForeignKey('years.id', ondelete='CASCADE'), nullable=False)
    students = db.relationship('Student', backref='group', lazy=True, \
                                cascade='all, delete', passive_deletes=True)

    def __repr__(self):
        return f'<group {self.group_name}>' 

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(32), nullable=False)
    unique = synonym('surname')
    name = db.Column(db.String(32), nullable=False)
    patronymic = db.Column(db.String(32), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)
    rk1_questions = db.relationship('RK1', backref='student', lazy=True, \
                                     cascade="all, delete", passive_deletes=True)
    rk1_status = db.Column(db.String(12), nullable=True)
    rk1_remaining_time = db.Column(db.Integer, nullable=True)
    rk1_score = db.Column(db.Integer, nullable=True)
    rk2_questions = db.relationship('RK2', backref='student', lazy=True, \
                                     cascade="all, delete", passive_deletes=True)
    rk2_status = db.Column(db.String(12), nullable=True)
    rk2_remaining_time = db.Column(db.Integer, nullable=True)
    rk2_score = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<surname {self.surname}>' 

class RK1(db.Model):
    __tablename__ = 'rk1'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=True)
    unique = synonym('question')
    student_answer = db.Column(db.String(64), nullable=True)
    correct_answer = db.Column(db.String(64), nullable=True)
    score = db.Column(db.Integer, nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'<question : {self.question}, correct_answer : {self.correct_answer}>'

class RK2(db.Model):
    __tablename__ = 'rk2'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=True)
    unique = synonym('question')
    student_answer = db.Column(db.String(64), nullable=True)
    correct_answer = db.Column(db.String(64), nullable=True)
    score = db.Column(db.Integer, nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'<question : {self.question}, correct_answer : {self.correct_answer}>'