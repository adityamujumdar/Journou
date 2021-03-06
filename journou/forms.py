from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from journou.models import Users
from flask_login import current_user

class RegistrationForm(FlaskForm):
	username=StringField('Username', validators=[DataRequired(), Length(min=2, max=15)])
	email=StringField('Email', validators=[DataRequired(), Email()])
	university=StringField('University', validators=[DataRequired(), Length(min=1, max=50)])

	password=PasswordField('Password', validators=[DataRequired()])
	confirm_password=PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit=SubmitField('Register')

	def validate_username(self, username):
		user = Users.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username is currently taken.')

	def validate_email(self, email):
		user = Users.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email is currently taken.')

class LoginForm(FlaskForm):
	email=StringField('Email', validators=[DataRequired(), Email()])
	password=PasswordField('Password', validators=[DataRequired()])
	remember=BooleanField('Remember Me')
	submit=SubmitField('Login')

class UpdateAccountForm(FlaskForm):
	username=StringField('Username', validators=[DataRequired(), Length(min=2, max=15)])
	email=StringField('Email', validators=[DataRequired(), Email()])
	university=StringField('University', validators=[DataRequired(), Length(min=1, max=50)])
	submit=SubmitField('Update Account')
	image=FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'svg'])])
	def validate_username(self, username):
		if username.data != current_user.username:
			user = Users.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username is currently taken.')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = Users.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Email is currently taken.')