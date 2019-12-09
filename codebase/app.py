# Author: Eli Hughes
# Purpose: Flask App for QuoteGIFr


from flask import Flask, render_template, request, redirect, url_for
from forms import MovieForm, QuoteForm, SelectMovieForm, SelectQuoteForm, FileLocationForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, and_
from datetime import datetime  # used to create filename of gif in this context
from quotegipher import gifEngine, getImage 
from giphypop import Giphy  # necessary for uploading to giphy.com
import webbrowser  # used to open giphy.com URL after upload
import os

app = Flask(__name__)

db_username = os.getenv('QGIFr_AWS_USERNAME')
db_password = os.getenv('QGIFr_AWS_PASSWORD')
app.config['SECRET_KEY'] = os.getenv('QGIFr_SECRET_KEY')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{username}:{password}@quotegifr-db2.csj8xbgbgcjk.us-east-1.rds.amazonaws.com:3306/quotegifrdb?charset=utf8mb4'.format(username=db_username, password=db_password)

db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    uid = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    # Capital 'T' in 'Timestamp' because we're referencing the Timestamp class
    timestamps = db.relationship('Timestamp', backref='movie', lazy=True)

    # for printing out a movie
    def __repr__(self):
        return f"Movie('{self.uid}', '{self.title}')"


class Timestamp(db.Model):
    __tablename__ = 'timestamp'
    uid = db.Column(db.Integer, primary_key=True, nullable=False)
    startime = db.Column(db.String(100), nullable=False)
    endtime = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    # Lowercase 'm' in 'movie.id' because we're referencing the tablename 'movie', not the class 'Movie'
    movieid = db.Column(db.Integer, db.ForeignKey('movie.uid'), nullable=False)

    # for printing out a timestamp
    def __repr__(self):
        return f"Timestamp('{self.uid}', '{self.movieid}', '{self.subtitle}', '{self.startime}', '{self.endtime}')"


@app.route("/", methods=["GET", "POST"])
@app.route("/film", methods=["GET", "POST"])
def homepage():
    # form for user to enter a movie name they come up with
    form = MovieForm()

    # if post data is submitted to this route, check it
    if request.method == 'POST':
        # check to see if form data under the name of 'movieName' was submitted
        if request.form.get('movieName'):
            # the user's film request
            filmRequest = request.form.get('movieName')

            filmResults = Movie.query.filter(Movie.title.like("%"+filmRequest+"%")).all()
            # filmResults = [filmRequest]

            # stores selection forms for all of the movie results the db returns
            filmForms = []
            # create the selection forms
            for result in filmResults:
                filmForms.append([result.title, SelectMovieForm(movieID=result.uid)])

            if filmForms == []:
                msg = 'Sorry, we couldn\'t find anything. Perhaps try searching again'
                return render_template('index.html', form=form, filmRequest=filmRequest, msg=msg)
            return render_template('index.html', form=form, filmRequest=filmRequest, filmForms=filmForms)

    # if no post data (or satisfactory post data) was submitted, render the base homepage
    return render_template('index.html', form=form)


@app.route("/quote", methods=["GET", "POST"])
def quotepage():

    # !IMPORTANT! 
    # only allow access to the quotepage if the user selected a movie from "homepage" or they just searched for
    # a quote using "quotepage"

    # if post data is submitted to this route, check it 
    if request.method == 'POST':

        # check to see if form data under the name of 'movieName' and 'quote' was submitted
        if request.form.get('movieID') and request.form.get('quote'):

            movieID = request.form.get('movieID')
            movie = Movie.query.get(movieID)
            movieName = movie.title
            quoteRequest = request.form.get('quote')

            # form for submitting a different quote request (search bar, essentially)
            form = QuoteForm(movieID=movieID)

            # do db stuff here...
            # the db query results using "quoteRequest"
            quoteResults = Timestamp.query.filter(and_(Timestamp.movieid == movieID, Timestamp.subtitle.like("%"+quoteRequest+"%"))).all()

            # stores selection forms for all of the quote results the db returns
            quoteForms = []
            for result in quoteResults:
                quoteForms.append([result.subtitle, SelectQuoteForm(quoteID=result.uid)])
            
            if quoteForms == []:
                msg = 'Sorry, we couldn\'t find anything. Perhaps try searching again'
                return render_template('quote.html', title='Quote', movieName='movieName', form=form, quoteRequest=quoteRequest, msg=msg)
            return render_template('quote.html', title='Quote', movieName=movieName, form=form, quoteRequest=quoteRequest, quoteForms=quoteForms)

        # if form data under the names of 'movieName' and 'quote' were not both submitted, check to see if 
        # just 'movieName' data was submitted (ie just came from "homepage")
        elif request.form.get('movieID'):
            movieID = request.form.get('movieID')
            movie = Movie.query.get(movieID)
            movieName = movie.title

            # form for submitting a quote request (search bar, essentially)
            form = QuoteForm(movieID=movieID)

            return render_template('quote.html', title='Quote', form=form, movieName=movieName)

    # redirect the user if they didn't select a movie from "homepage" or search for a quote on "quotepage" 
    # (ie no correct post data submitted)
    return redirect(url_for('homepage'))


@app.route("/generate", methods = ["GET", "POST"])
def generateGIFpage():
    # if post data submitted, print it out (will use this data to generate a gif)
    if request.method == 'POST':
        if request.form.get('quoteID'):
            quoteID = request.form.get('quoteID')
            timestamp = Timestamp.query.get(quoteID)

            starttime = timestamp.startime
            endtime = timestamp.endtime

            movieID = timestamp.movieid
            movieName = Movie.query.get(movieID).title
            videofileloc = 'media/' + movieName + '.mp4'
            strfileloc = 'media/' + movieName + '.srt'

            outfile = "static/outfile"
            if not os.path.exists(outfile+"/"):
                os.mkdir(outfile+"/")
            gif_outfileloc = (outfile + "/GIF_{}.gif").format(datetime.now().strftime("%H_%M_%S"))
            retcode = gifEngine(starttime, endtime, videofileloc, strfileloc,  gif_outfileloc)
            if retcode == 0:
                form = FileLocationForm(gifLocation=gif_outfileloc)
                return render_template('generate.html', gif_outfileloc=gif_outfileloc[7:], form=form)
            else:
                return redirect(url_for('homepage')) # This needs to go to an error page of some kind, GIF was not created
    return redirect(url_for('homepage'))

    @app.route("/upload", methods=["GET", "POST"])
    def generateGIFpage():
        if request.method == 'POST':
            print(request.form.errors)
            if request.form.get('gifLocation'):
                gifLocation = request.form.get('gifLocation')
                giphyobj = Giphy('iTmKRrpWJUCpn6nWMSIp42gmkXA6hpfh')
                # response (below) is the URL for our giphy upload
                response = giphyobj.upload([], gifLocation, username="QuoteGIFr")
                return render_template('upload.html', response=response)
        return redirect(url_for('homepage'))


# Can now run app directly ('python app.py' command in bash) without 
# having to set Flask environment variables every time (ie. 'export FLASK_APP=app.py' 
# command in bash).
if __name__ == '__main__':
    app.run(debug=True)

