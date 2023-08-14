from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload
from app.models.data import Data
from app.models.job import Job
from . import valid
from app import db

jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')

@jobs_bp.route('', methods=['POST'])
def create_job():
    request_body = request.get_json()
    valid.validate_entry(Job, request_body)
    
    job_id = Job.query.filter_by(job_id=request_body['job_id']).first()
    if job_id:
        return {'msg': f'Job with job_id {job_id} already exist'}, 200
    
    new_entry = Job.from_dict(request_body)
    
    db.session.add(new_entry)
    db.session.commit()
    
    return new_entry.to_dict(), 201

@jobs_bp.route('', methods=['GET'])
def get_jobs():
    
    title_query = request.args.get('title')
    location_query = request.args.get('location')
    company_query = request.args.get('company')
    days_ago = request.args.get('days_ago', type=int)
    
    # Query the database for jobs posted since the specified number of days ago
    # jobs = Job.query.filter(Job.posted_date >= posted_since).all()
    
    # if title_query:
    #     jobs = Job.query.filter(Job.title.ilike('%'+title_query.strip()+'%')).order_by(Job.data.fetch_date.desc())
    # elif title_query and location_query:
    #     jobs = Job.query.filter(Job.title.ilike('%'+title_query.strip()+'%'), 
    #                             Job.location.ilike('%'+location_query.strip()+'%')
    #                             ).order_by(Job.data.fetch_date.desc())
    # elif title_query and location_query: #and posted_since:
    #     jobs = Job.query.filter(Job.title.ilike('%'+title_query.strip()+'%'), 
    #                             Job.location.ilike('%'+location_query.strip()+'%'),
    #                             # Job.data.fetch_date >= posted_since
    #                             ).order_by(Job.data.fetch_date.desc())
    # if company_query:
    #     jobs = Job.query.filter(Job.company.ilike('%'+company_query.strip()+'%')).order_by(Job.data.fetch_date.desc())
    # elif company_query and location_query:
    #     jobs = Job.query.filter(Job.company.ilike('%'+company_query.strip()+'%'), 
    #                             Job.location.ilike('%'+location_query.strip()+'%')
    #                             ).order_by(Job.data.fetch_date.desc())
    # elif company_query and location_query:# and posted_since:       
    #     jobs = Job.query.filter(Job.company.ilike('%'+company_query.strip()+'%'), 
    #                             Job.location.ilike('%'+location_query.strip()+'%'),
    #                             # Job.data.fetch_date >= posted_since
    #                             # Job.data.fetch_date.ilike('%'+fetched.strip()+'%')
    #                             ).order_by(Job.data.fetch_date.desc())
    # # elif posted_since:
    # #     Job.query.filter(Job.posted_date >= posted_since).order_by(Job.data.fetch_date.desc()).all()
    # else:
    #     # jobs = Job.query.order_by(Job.data.fetch_date.desc()).all()
    #     jobs = (
    #         db.session.query(Job)
    #         .join(Data)
    #         .options(joinedload(Job.data))
    #         .order_by(Data.fetch_date.desc())
    #         .all()
    #     )
    
    query = db.session.query(Job).join(Data).options(joinedload(Job.data)).order_by(Data.fetch_date.desc())

    if title_query:
        query = query.filter(Job.title.ilike('%'+title_query.strip()+'%'))
    if location_query:
        query = query.filter(Job.location.ilike('%'+location_query.strip()+'%'))
    if company_query:
        query = query.filter(Job.company.ilike('%'+company_query.strip()+'%'))
    if days_ago:
        posted_date = datetime.utcnow() - timedelta(days=int(days_ago))
        # query = query.filter(Job.data.fetch_date <= posted_date)
        # posted_date = datetime.utcnow() - timedelta(days=posted_since)
        
        # Convert to the same format as the fetch_date in the database
        posted_date_str = posted_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
        query = query.filter(Data.fetch_date <= posted_date_str)


    # Execute the final query
    jobs = query.all()

    return jsonify([entry.to_dict() for entry in jobs]), 200

@jobs_bp.route('/delete_all', methods=['DELETE'])
def delete_all_jobs():
    Job.query.delete()
    db.session.commit()
    
    return {'details': 'All jobs successfully deleted'}, 200