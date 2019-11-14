from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://***REMOVED***:***REMOVED***@quotegifr-db.csj8xbgbgcjk.us-east-1.rds.amazonaws.com:3306/quotegifr-db'
db = SQLAlchemy(app)



class Movie(db.Model):
    __tablename__ = 'movie'
    uid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    timestamps = db.relationship("Child")

class Timestamp(db.Model):
    __tablename__ = 'timestamp'
    uid = db.Column(db.Integer, primary_key=True)
    subtitle = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.String(100), nullable=False)
    movieid = (db.Integer, db.ForeignKey('movie.uid'))

app.run
db.create_all()