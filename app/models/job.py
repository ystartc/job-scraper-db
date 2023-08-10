from sqlalchemy import func
from app import db

class Job (db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.String(20))
    title = db.Column(db.String(100))
    company = db.Column(db.String(100))
    location = db.Column(db.String(100))
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
            'data_id': self.data.id,
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
            salary=request_body.get('salary', None),
            data_id=request_body['data_id']
        )
        
        return job