# Author: Eli Hughes
# Purpose: Flask App for QuoteGIFr

from flask import Flask, render_template, request, redirect, url_for
from forms import MovieForm, QuoteForm, SelectMovieForm, SelectQuoteForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '***REMOVED***'

@app.route("/", methods = ["GET", "POST"])
@app.route("/film", methods = ["GET", "POST"])
def homepage():
    # form for user to enter a movie name they come up with
    form = MovieForm()

    # if post data is submitted to this route, check it
    if request.method == 'POST':
        # check to see if form data under the name of 'movieName' was submitted
        if request.form.get('movieName'):
            # the user's film request
            filmRequest = request.form.get('movieName')

            # do db stuff here...
            # the db query results using "filmRequest"
            filmResults = [filmRequest]

            # stores selection forms for all of the movie results the db returns
            filmForms = []
            # create the selection forms
            for result in filmResults:
                filmForms.append([result, SelectMovieForm(movieName = result)])
            return render_template('index.html', form = form, filmRequest = filmRequest, filmForms = filmForms)

    # if no post data (or satisfactory post data) was submitted, render the base homepage
    return render_template('index.html', form = form)

@app.route("/quote", methods = ["GET", "POST"])
def quotepage():

    # !IMPORTANT! 
    # only allow access to the quotepage if the user selected a movie from "homepage" or they just searched for
    # a quote using "quotepage"

    # if post data is submitted to this route, check it 
    if request.method == 'POST':

        # check to see if form data under the name of 'movieName' and 'quote' was submitted
        if request.form.get('movieName') and request.form.get('quote'):

            movieName = request.form.get('movieName')
            quoteRequest = request.form.get('quote')

            # form for submitting a different quote request (search bar, essentially)
            form = QuoteForm(movieName = movieName)

            # do db stuff here...
            # the db query results using "quoteRequest"
            quoteResults = [quoteRequest]

            # stores selection forms for all of the quote results the db returns
            quoteForms = []
            for result in quoteResults:
                quoteForms.append([result, SelectQuoteForm(movieName = movieName, quote = result)])
            return render_template('quote.html', title = 'Quote', form = form, movieName = movieName, quoteRequest = quoteRequest, quoteForms = quoteForms)

        # if form data under the names of 'movieName' and 'quote' were not both submitted, check to see if 
        # just 'movieName' data was submitted (ie just came from "homepage")
        elif request.form.get('movieName'):
            movieName = request.form.get('movieName')

            # form for submitting a quote request (search bar, essentially)
            form = QuoteForm(movieName = movieName)

            movieName = request.form.get('movieName')
            return render_template('quote.html', title = 'Quote', form = form, movieName = movieName)

    # redirect the user if they didn't select a movie from "homepage" or search for a quote on "quotepage" 
    # (ie no correct post data submitted)
    return redirect(url_for('homepage'))

@app.route("/generate", methods = ["GET", "POST"])
def generateGIFpage():
    # if post data submitted, print it out (will use this data to generate a gif)
    if request.method == 'POST':
        movie = request.form.get('movieName')
        quote = request.form.get('quote')
        return render_template('generate.html', movie = movie, quote = quote)

    return redirect(url_for('homepage'))

# Can now run app directly ('python app.py' command in bash) without 
# having to set Flask environment variables every time (ie. 'export FLASK_APP=app.py' 
# command in bash).
if __name__ == '__main__':
    app.run(debug=True)

