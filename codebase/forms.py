# Author: Eli Hughes
# Purpose: Form classes from which form objects will be made in "app.py"
#          and presented in "index.html", and "quote.html"

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired

# class for a form for searching for a movie
class MovieForm(FlaskForm):
    movieName = StringField('Movie Name', validators = [DataRequired()])
    submit = SubmitField('Search for this film')

# class for a form for searching for a quote
class QuoteForm(FlaskForm):
    movieName = HiddenField()
    quote = StringField('Film Quote', validators = [DataRequired()])
    submit = SubmitField('Search for this quote')

# class for a form for selecting an individual movie
class SelectMovieForm(FlaskForm):
    movieName = HiddenField()
    submit = SubmitField('Select')

# class for a form for selecting an individual quote
class SelectQuoteForm(FlaskForm):
    movieName = HiddenField()
    quote = HiddenField()
    submit = SubmitField('Select')

