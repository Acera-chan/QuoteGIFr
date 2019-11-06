# Author: Eli Hughes
# Date Last Modified: 10/8/19
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

    # if the user submitted a movie request, handle it
    if request.method == 'POST':
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
    return render_template('index.html', form = form)

@app.route("/quote", methods = ["GET", "POST"])
def quotepage():
    if request.method == 'POST':
        movieName = request.form.get('movieName')
        form = QuoteForm(movieName = movieName)
        if request.form.get('quote'):
            quoteRequest = request.form.get('quote')
            quoteResults = [quoteRequest]
            quoteForms = []
            for result in quoteResults:
                quoteForms.append([result, SelectQuoteForm(movieName = movieName, quote = result)])
            return render_template('quote.html', title = 'Quote', form = form, movieName = movieName, quoteRequest = quoteRequest, quoteForms = quoteForms)
        
        else:
            return render_template('quote.html', title = 'Quote', form = form, movieName = movieName)

    return redirect(url_for('homepage'))

@app.route("/generate", methods = ["GET", "POST"])
def generateGIFpage():
    if request.method == 'POST':
        movie = request.form.get('movieName')
        quote = request.form.get('quote')

        if movie == 'An Ideal Husband 1947' and quote == 'Surely. You have nothing to conceal?':
            starttime = '00:42:16,160'
            endtime = '00:42:18,036'

            videofileloc = r"G:\Users\Eli\Projects\QuoteGIFr_proj\An Ideal Husband 1947.mp4"
            strfileloc = r"G:\Users\Eli\Projects\QuoteGIFr_proj\An Ideal Husband 1947.srt"
            outfile = r"G:\Users\Eli\Projects\QuoteGIFr_proj\outfile"

            
        return render_template('generate.html', movie = movie, quote = quote)

    return redirect(url_for('homepage'))

# Can now run app directly ('python app.py' command in bash) without 
# having to set Flask environment variables every time (ie. 'export FLASK_APP=app.py' 
# command in bash).
if __name__ == '__main__':
    app.run(debug=True)

