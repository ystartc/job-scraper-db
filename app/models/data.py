from sqlalchemy import func
from app import db

class Data (db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    html = db.Column(db.Text)
    user_agent = db.Column(db.String)
    status = db.Column(db.String)
    url = db.Column(db.String)
    fetch_date = db.Column(db.Date, default=func.now())
    jobs = db.relationship('Job', back_populates='data', lazy=True)