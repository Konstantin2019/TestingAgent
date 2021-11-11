from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from wtforms import SelectField, StringField, SubmitField, PasswordField

class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass

class StudentAuth(FlaskForm):
    surname = StringField(label=('Фамилия:'), validators=[DataRequired()])
    name = StringField(label=('Имя:'), validators=[DataRequired()])
    patronymic = StringField(label=('Отчество: '), validators=[DataRequired()])
    group = NonValidatingSelectField(label=('Группа'), choices=[])
    test = NonValidatingSelectField(label=('Рубежный контроль'), choices=[('rk1','РК №1'), ('rk2','РК №2')])
    teacher = NonValidatingSelectField(label=('Преподаватель'), choices=[('potapov','Потапов К.Г.'), ('tumakova','Тумакова Е.В.')])
    submit = SubmitField(label=('Подтвердить'))
    excluded_chars = " |*?!'^+%&amp;/()=}][{$#123456789\""

    def validate_surname(self, surname):
        finded_exlc = []
        for char in surname.data:
            if char in self.excluded_chars:
                finded_exlc.append(char)
        if finded_exlc:
            raise ValidationError(f"Недопустимые сивмолы {finded_exlc}.")
    
    def validate_name(self, name):
        finded_exlc = []
        for char in name.data:
            if char in self.excluded_chars:
                finded_exlc.append(char)
        if finded_exlc:
            raise ValidationError(f"Недопустимые сивмолы {finded_exlc}.")

    def validate_patronymic(self, patronymic):
        finded_exlc = []
        for char in patronymic.data:
            if char in self.excluded_chars:
                finded_exlc.append(char)
        if finded_exlc:
            raise ValidationError(f"Недопустимые сивмолы {finded_exlc}.")

class AdminAuth(FlaskForm):
    login = StringField(label=('Имя пользователя:'))
    password = PasswordField(label=('Пароль:'))
    submit = SubmitField(label=('Подтвердить'))