from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, DateField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError


def phone_validator(form, field):
    phone = field.data
    digits = "".join(c for c in phone if c.isdigit())
    if len(digits) != 11:
        raise ValidationError("Номер телефона должен содержать 11 цифр")
    if digits[0] not in ("7", "8"):
        raise ValidationError("Номер должен начинаться с +7 или 8")
    if not all(c.isdigit() for c in digits[1:]):
        raise ValidationError("Номер телефона должен содержать только цифры")
    formatted = f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
    field.data = formatted


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Подтвердите пароль", validators=[DataRequired()])


class ProfileForm(FlaskForm):
    avatar = FileField("Фото профиля", validators=[
        FileAllowed(["jpg", "jpeg", "png"], "Только изображения!")
    ])


class BookingForm(FlaskForm):
    date = DateField("Дата", validators=[DataRequired()], format="%Y-%m-%d")
    time_from = StringField("С", validators=[DataRequired()])
    time_to = StringField("До", validators=[DataRequired()])
    table_number = StringField("Номер столика", validators=[DataRequired()])
    phone = StringField("Телефон", validators=[DataRequired(), phone_validator])
    special_requests = TextAreaField("Особые пожелания", validators=[Optional()])
