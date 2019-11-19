from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from quotegipher import SrtFile

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://***REMOVED***:***REMOVED***@quotegifr-db2.csj8xbgbgcjk.us-east-1.rds.amazonaws.com:3306/quotegifrdb'
db = SQLAlchemy(app)

path_media_folder = '\\PATH\\TO\\MEDIA\\'
# Add ".mp4" or ".srt" to the strings below
# to point to the associated files
path_an_ideal_husband = path_media_folder + "An Ideal Husband 1947"
path_dressed_to_kill = path_media_folder + "Dressed to Kill 1946"
path_the_last_time = path_media_folder + "The Last Time I Saw Paris 1954"
# The objects below contain methods
# to extract all data from the associated
# SRT files. >>>Replace or assign movieid's to the tuples.<<<
srt_list = [("movieid_an_ideal", SrtFile(path_an_ideal_husband + ".srt"))]
srt_list.append(("movieid_dressed", SrtFile(path_dressed_to_kill + ".srt")))
srt_list.append(("movieid_the_last", SrtFile(path_the_last_time + ".srt")))


""" class Movie(db.Model):
    def __init__(self, uid, title):
        self.uid = uid
        self.title = title
    __tablename__ = 'movie'
    uid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    timestamps = db.relationship("Timestamp", back_populates='movie')


class Timestamp(db.Model):
    def __init__(self, uid, subtitle, timestamp, movieid):
        self.uid = uid
        self.subtitle = subtitle
        self.timestamp = timestamp
        self.movieid = movieid
    __tablename__ = 'timestamp'
    uid = db.Column(db.Integer, primary_key=True)
    subtitle = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.String(100), nullable=False)
    movieid = db.Column(db.Integer, db.ForeignKey('movie.uid'))
    movie = db.relationship("Movie", back_populates='movie') """

class Movie(db.Model):
    __tablename__ = 'movie'
    uid = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    # Capital 'T' in 'Timestamp' because we're referencing the Timestamp class
    timestamps = db.relationship('Timestamp', backref = 'movie', lazy = True)

    # for printing out a movie
    def __repr__(self):
        return f"User('{self.uid}', '{self.title}')"


class Timestamp(db.Model):
    __tablename__ = 'timestamp'
    uid = db.Column(db.Integer, primary_key=True)
    startime = db.Column(db.String(100), nullable=False)
    endtime = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    # Lowercase 'm' in 'movie.id' because we're referencing the tablename 'movie', not the class 'Movie'
    movieid = db.Column(db.Integer, db.ForeignKey('movie.uid'), nullable = False)

    # for printing out a timestamp
    def __repr__(self):
        return f"User('{self.uid}', '{self.movieid}', '{self.subtitle}', '{self.timestamp}')"


app.run
db.create_all()

# An attempt to add timestamps to db,
# will need to setup movie relation first, though
for tuple_item in srt_list:
    movieid = tuple_item[0]  # use this to add movieid once implemented
    srt_file = tuple_item[1]
    for key in srt_file.lines:
        subtitle = srt_file.getLineCaption(key)
        start_time = srt_file.getLineStartTime(key)
        end_time = srt_file.getLineEndTime(key)
        timestamp = Timestamp(key, subtitle, start_time+":"+end_time, movieid)
        db.session.add(timestamp)

results = db.session.query(Timestamp).filter_by(uid=1)
for row in results:
    print(row.subtitle)
