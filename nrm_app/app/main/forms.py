from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo

class AddUserForm(FlaskForm):
    user_login = StringField('Login studenta (nr indeksu)', validators=[DataRequired(),])
    submit = SubmitField('Generuj konto')

class AddTeacherForm(FlaskForm):
    teacher_login = StringField('Login wykładowcy (np email)', validators=[DataRequired(),])
    submit = SubmitField('Generuj konto')