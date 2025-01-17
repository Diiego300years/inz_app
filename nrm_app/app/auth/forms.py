from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from app.models.admin import AdminModel


class LoginForm(FlaskForm):

    email = StringField('e-mail', validators=[DataRequired(),
                        Length(1,64),
                        Email()])

    password = PasswordField('password', validators=[
        DataRequired(),
        Length(8,64)])

    remember = BooleanField('remember me')

    submit = SubmitField('submit')


class RegistrationForm(FlaskForm):
    email = StringField('e-mail', validators=[DataRequired(), Length(4,32), Email()])

    username = StringField('username', validators=[
        DataRequired(),
        Length(4,32),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Your username can consist only letters, digits, dots and _ signs')])
    password = PasswordField('password', validators=[
        DataRequired(),
        EqualTo('password2', message='Passwords must be exactly the same')])
    password2 = PasswordField('confirm password', validators=[
        DataRequired(),])
    submit = SubmitField('register')

    def validate_email(self, field):
        if AdminModel.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('This email address is already registered')

    def validate_username(self, field):
        if AdminModel.query.filter_by(name=field.data).first():
            raise ValidationError('This username is already in use.')

