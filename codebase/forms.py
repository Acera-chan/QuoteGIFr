# Author: Eli Hughes
# Purpose: Form classes from which form objects will be made in "app.py"
#          and presented in "index.html", and "quote.html"

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired


# class for a form for searching for a movie
class MovieForm(FlaskForm):
    movieName = StringField('Movie Name', validators=[DataRequired()], render_kw={"placeholder": "Enter movie name..."})
    submit = SubmitField('Submit')


# class for a form for searching for a quote
class QuoteForm(FlaskForm):
    movieID = HiddenField()
    quote = StringField('Film Quote', validators=[DataRequired()], render_kw={"placeholder": "Enter quote text..."})
    submit = SubmitField('Submit')


# class for a form for selecting an individual movie
class SelectMovieForm(FlaskForm):
    movieID = HiddenField()
    submit = SubmitField('Select')


# class for a form for selecting an individual quote
class SelectQuoteForm(FlaskForm):
    quoteID = HiddenField()
    submit = SubmitField('Select')


# class for sending along a file path used for uploading a gif
class FileLocationForm(FlaskForm):
    gifLocation = HiddenField()
    submit = SubmitField('Upload to GIPHY')
