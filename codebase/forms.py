from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired

class MovieForm(FlaskForm):
    movieName = StringField('Movie Name', validators = [DataRequired()])
    submit = SubmitField('Search for this film')

class QuoteForm(FlaskForm):
    movieName = HiddenField()
    quote = StringField('Film Quote', validators = [DataRequired()])
    submit = SubmitField('Search for this quote')

class SelectMovieForm(FlaskForm):
    movieName = HiddenField()
    submit = SubmitField('Select')

class SelectQuoteForm(FlaskForm):
    movieName = HiddenField()
    quote = HiddenField()
    submit = SubmitField('Select')

