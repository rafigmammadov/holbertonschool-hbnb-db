from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import jsonify
from functools import wraps

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if not claims.get('is_admin'):
            return jsonify({"msg": "Administration rights required"}), 403
        return fn(*args, **kwargs)
    return wrapper
