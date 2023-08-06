from sqlalchemy import func
from app import db

class Job (db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer)
    title = db.Column(db.String)
    fetch_date = db.Column(db.Date, default=func.now())
    company = db.Column(db.String)
    location = db.Column(db.String)
    about = db.Column(db.Text)
    salary = db.Column(db.String, nullable=True)
    data_id = db.Column(db.Integer, db.ForeignKey('data.id'))
    data = db.relationship('Data', back_populates='jobs')