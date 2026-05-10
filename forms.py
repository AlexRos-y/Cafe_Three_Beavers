from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, DateField
from wtforms.validators import DataRequired, Email, Length, Optional


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired()])


class ProfileForm(FlaskForm):
    avatar = FileField('Фото профиля', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Только изображения!')
    ])


class BookingForm(FlaskForm):
    date = DateField('Дата', validators=[DataRequired()], format='%Y-%m-%d')
    time_from = StringField('С', validators=[DataRequired()])
    time_to = StringField('До', validators=[DataRequired()])
    table_number = StringField('Номер столика', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    special_requests = TextAreaField('Особые пожелания', validators=[Optional()])
