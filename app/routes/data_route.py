from flask import Blueprint, jsonify, request
from app.models.data import Data
from app.models.job import Job
from . import valid
from app import db


data_bp = Blueprint('data', __name__, url_prefix='/data')


@data_bp.route('', methods=['POST'])
def create_entry():
    request_body = request.get_json()
    valid_request = valid.validate_entry(Data, request_body)

    new_entry = Data.from_dict(valid_request)
    
    db.session.add(new_entry)
    db.session.commit()
    
    return new_entry.to_dict(), 201

@data_bp.route('', methods=['GET'])
def get_data():
    status_query = request.args.get('status')
    
    if status_query:
        data = Data.query.filter(Data.status.ilike('%'+status_query.strip()+'%'))
    else:
        data = Data.query.all()
    
    return jsonify([entry.to_dict() for entry in data]), 200

@data_bp.route('/delete_all', methods=['DELETE'])
def delete_all_data():
    Data.query.delete()
    db.session.commit()
    
    return {'details': 'All data successfully deleted'}, 200