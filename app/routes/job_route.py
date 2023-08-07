from flask import Blueprint, jsonify, request
from app.models.job import Job
from . import valid
from app import db

jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')

@jobs_bp.route('', methods=['POST'])
def create_job():
    request_body = request.get_json()
    valid.validate_entity(Job, request_body)
    
    new_entry = Job.from_dict(request_body)
    
    db.session.add(new_entry)
    db.session.commit()
    
    return new_entry.to_dict(), 201

@jobs_bp.route('', methods=['GET'])
def get_jobs():
    title_query = request.args.get('title')
    
    if title_query:
        jobs = Job.query.filter(Job.title.ilike('%'+title_query.strip()+'%'))
    else:
        jobs = Job.query.all()
    
    return jsonify([entry.to_dict() for entry in jobs]), 200