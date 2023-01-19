from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, TextAreaField, FloatField, URLField, \
    HiddenField
from wtforms.validators import DataRequired, EqualTo, Length


class RegisterForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired(), EqualTo('confirm',
                                                                              message='Passwords must match.')])
    confirm = PasswordField('Repeat Password:')
    username = StringField('Username:', validators=[DataRequired()])
    submit = SubmitField('Sign me up!')


class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')


class SearchMovieForm(FlaskForm):
    title = StringField('Enter the Title of the Movie:', validators=[DataRequired()])
    submit = SubmitField('Search')


class UpdateMovieForm(FlaskForm):
    id = HiddenField(label='id')
    rating = FloatField('Your Rating Out of 10 e.g. 7.5:', validators=[DataRequired()])
    review = TextAreaField('Your review', validators=[DataRequired(), Length(max=250)])
    submit = SubmitField('Done')


class AddMovieForm(FlaskForm):
    id = HiddenField(label='id')
    rating = FloatField('Your Rating Out of 10 e.g. 7.5:', validators=[DataRequired()])
    review = TextAreaField('Your review', validators=[DataRequired(), Length(max=250)])
    submit = SubmitField('Done')
