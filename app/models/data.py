from app import db

class Data (db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    html = db.Column(db.Text)
    browser = db.Column(db.String)
    type = db.Column(db.String)
    jobs = db.relationship('Job', back_populates='data', lazy=True)