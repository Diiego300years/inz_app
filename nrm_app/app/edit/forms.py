from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired

class DeleteUserWithFolderForm(FlaskForm):
    username = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Usuń z folderem')

class DeleteUserWithoutFolderForm(FlaskForm):
    username = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Usuń bez folderu')

class AddUserToGroupForm(FlaskForm):
    username = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Dodaj do grupy')
    # group = SelectField('Wybierz grupę', choices=[
    #     ('samba_users', 'samba_users'),
    #     ('samba_admins', 'samba_admins')
    # ], validators=[DataRequired()])
    group = SelectField('Wybierz grupę', choices=[], validators=[DataRequired()])

