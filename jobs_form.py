from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SelectMultipleField, BooleanField, SubmitField
from wtforms.validators import InputRequired

class AddJobForm(FlaskForm):
    job_title = StringField('Название работы', validators=[InputRequired()])
    team_leader = SelectField('Ответственный', coerce=int, validators=[InputRequired()])
    work_size = FloatField('Продолжительность (часы)', validators=[InputRequired()])
    collaborators = SelectMultipleField('Список участников', coerce=int, validators=[InputRequired()])
    is_finished = BooleanField('Завершена')
    submit = SubmitField('Добавить работу')

class EditJobForm(FlaskForm):
    job = StringField('Название работы')
    team_leader = SelectField('Ответственный', coerce=int)
    work_size = FloatField('Продолжительность (часы)')
    collaborators = SelectMultipleField('Список участников', coerce=int)
    is_finished = BooleanField('Завершена')
    submit = SubmitField('Сохранить изменения')
    delete = SubmitField('Удалить работу')
