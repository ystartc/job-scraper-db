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