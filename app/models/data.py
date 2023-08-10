from sqlalchemy.sql import func
from datetime import datetime
from app import db

class Data (db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    html = db.Column(db.Text)
    status = db.Column(db.String)
    url = db.Column(db.String)
    # fetch_date = db.Column(db.Date, default=func.current_date())
    fetch_date = db.Column(db.Date, default=None, nullable=True)
    jobs = db.relationship('Job', back_populates='data', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'html': self.html,
            'status': self.status,
            'url': self.url,
            'fetch_date': self.fetch_date
        }

    @classmethod
    def get_attributes(cls):
        return 'html', 'status', 'url'
    
    @classmethod
    def from_dict(cls, request_body):
        if 'fetch_date' in request_body:
            data = cls(
            html=request_body['html'],
            status=request_body['status'],
            url=request_body['url'],
            fetch_date=datetime.strptime(request_body['fetch_date'], '%d %b %Y').date()
        )
        else:
            data = cls(
                html=request_body['html'],
                status=request_body['status'],
                url=request_body['url'],
                fetch_date=func.current_date()
            )
        
        return data