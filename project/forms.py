from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired, Email

class FindFriendForm(FlaskForm):
    email = EmailField('Friend\'s email', validators=[DataRequired(), Email()])
    submit_find_friend = SubmitField('Find friend')

class SendRequest(FlaskForm):
    friend_id = IntegerField()
    submit = SubmitField('Send request')

