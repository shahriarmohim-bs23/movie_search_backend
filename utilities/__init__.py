
from utilities.jwt import decode
from flask import jsonify,make_response,request
from functools import wraps


def token_required(func):
    @wraps(func)
    def decorator(*args,**kwargs):
        token = request.headers.get('token')
        if not token:
           error = {'message':'Token not provided'}
           return make_response(jsonify(error),401)
        try:
            decode(token)
            return func(*args,**kwargs)
        except Exception:
             error = {'message':'Token not valid'}
             return make_response(jsonify(error),401)
 
    return decorator