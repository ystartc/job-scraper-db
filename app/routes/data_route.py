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