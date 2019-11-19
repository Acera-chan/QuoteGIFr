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
# SRT files
srt_an_ideal_husband = SrtFile(path_an_ideal_husband + ".srt")
srt_dressed_to_kill = SrtFile(path_dressed_to_kill + ".srt")
srt_the_last_time = SrtFile(path_the_last_time + ".srt")


class Movie(db.Model):
    def __init__(self, uid, title):
        self.uid = uid
        self.title = title
    __tablename__ = 'movie'
    uid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    # timestamps = db.relationship("Timestamp", backref='movie')


class Timestamp(db.Model):
    def __init__(self, uid, subtitle, timestamp):
        self.uid = uid
        self.subtitle = subtitle
        self.timestamp = timestamp
        # self.movieid = movieid
    __tablename__ = 'timestamp'
    uid = db.Column(db.Integer, primary_key=True)
    subtitle = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.String(100), nullable=False)
    # movieid = db.Column(db.Integer, db.ForeignKey('movie.uid'))
    # movie = db.relationship(Movie, backref='movie')


app.run
db.create_all()
timestamp = Timestamp(1, "hello world", "1:2")
db.session.add(timestamp)
results = db.session.query(Timestamp).filter_by(uid=1)
for row in results:
    print(row.subtitle)
