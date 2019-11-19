from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from quotegipher import SrtFile

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://***REMOVED***:***REMOVED***@quotegifr-db2.csj8xbgbgcjk.us-east-1.rds.amazonaws.com:3306/quotegifrdb'
db = SQLAlchemy(app)

media_folder = '\\PATH\\TO\\MEDIA\\'
srt_an_ideal_husband = SrtFile(media_folder + "An Ideal Husband 1947.srt")
srt_dressed_to_kill = SrtFile(media_folder + "Dressed to Kill 1946.srt")
srt_the_last_time = SrtFile(media_folder + "The Last Time I Saw Paris 1954.srt")


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
