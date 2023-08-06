from flask import abort, make_response
import requests
import os


def validate_id(model, id):
    if not id.isnumeric():
        abort(make_response({'Error': f'{id} is invalid'}, 400))
    
    entity = model.query.get(id)
    if not entity:
        abort(make_response({'Not found': f'No {model.__name__} with id#{id} is found'}, 404))
        
    return entity

def validate_entry(model, request_body):
    for atr in model.get_attributes():
        if atr not in request_body:
            abort(make_response({'details': f'Missing data - {atr} is not provided'}, 400))
    
    return request_body