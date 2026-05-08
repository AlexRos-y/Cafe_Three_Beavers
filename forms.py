from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, FloatField, SelectField, DateField, TimeField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired()])

class ReviewForm(FlaskForm):
    rating = SelectField('Оценка', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], validators=[DataRequired()])
    text = TextAreaField('Отзыв', validators=[DataRequired(), Length(min=10)])

class BookingForm(FlaskForm):
    date = DateField('Дата', validators=[DataRequired()], format='%Y-%m-%d')
    time = TimeField('Время', validators=[DataRequired()], format='%H:%M')
    guests = IntegerField('Количество гостей', validators=[DataRequired(), NumberRange(min=1, max=20)])
    special_requests = TextAreaField('Особые пожелания', validators=[Optional()])

class OrderForm(FlaskForm):
    delivery_address = StringField('Адрес доставки', validators=[DataRequired()])
    latitude = FloatField('Широта', validators=[Optional()])
    longitude = FloatField('Долгота', validators=[Optional()])