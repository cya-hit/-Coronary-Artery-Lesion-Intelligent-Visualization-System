from flask import Blueprint
from flask import jsonify,request
from itsdangerous import  TimedJSONWebSignatureSerializer
from flask import current_app,g
import functools,logging


api = Blueprint('api',__name__)

def login_required(*permission):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            try:
                token = request.headers.get('Authorization')
                s = TimedJSONWebSignatureSerializer(current_app.config['USER_TOKEN_KEY'])
                data = s.loads(token)
            except Exception  as e:
                return jsonify({'status': 102, 'data': 'token校验失败'})
            g.username = data['id']
            per = data['permission']
            if len(permission) > 0:
                allowed = any([p in per for p in permission])
                if not allowed:
                    return jsonify({'status': 105, 'data': '权限错误'})

            return func(*args, **kw)
        return wrapper
    return decorator


@api.errorhandler(Exception)
def error_handler(e):
    logging.exception(e)
    data = {
        "status": 101,
        "data": "服务器内部错误"
    }
    return jsonify(data)

# from . import dataapi
# from . import userapi
