from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class NotepadForm(FlaskForm):
    # titulo
    title = StringField('Title', validators=[DataRequired(), Length(max=256)])
    # cuerpo
    body = TextAreaField('Body', validators=[DataRequired()])
    # submit
    submit = SubmitField('Save notepad')
