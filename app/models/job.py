from sqlalchemy import func
from app import db

class Job (db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer)
    title = db.Column(db.String)
    company = db.Column(db.String)
    location = db.Column(db.String)
    about = db.Column(db.Text)
    salary = db.Column(db.String, nullable=True)
    data_id = db.Column(db.Integer, db.ForeignKey('data.id'))
    data = db.relationship('Data', back_populates='jobs')
    
    def to_dict(self):
        job_dict = {
            'id': self.id,
            'job_id': self.job_id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'about': self.about,
            'fetch_date': self.data.fetch_date,
            'data_id': self.data_id,
        }
        
        if self.salary:
            job_dict['salary'] = self.salary
            
        return job_dict
    
    @classmethod
    def get_attributes(cls):
        return 'job_id', 'title', 'company', 'location', 'about'
    
    @classmethod
    def from_dict(cls, request_body):
        job = cls(
            job_id=request_body['job_id'],
            title=request_body['title'],
            company=request_body['company'],
            location=request_body['location'],
            about=request_body['about'],
            data_id=request_body['data_id'],
            salary=request_body.get('salary', None)
        )
        
        return job