import json
from datetime import datetime, date
from decimal import Decimal

from starlette.responses import JSONResponse

from bebinca.utils.resp_util import BaseResponse


class JsonExtendEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, (tuple, list, datetime)):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, bytes):
            return obj.decode('utf-8')
        return super().default(obj)


class JsonExtendResponse(JSONResponse):

    def render(self, content):
        return json.dumps(content, cls=JsonExtendEncoder).encode('utf-8')


def jsonify(*args, **kwargs):
    if args and kwargs:
        raise TypeError('jsonify() behavior undefined when passed both args and kwargs')
    elif len(args) == 1:
        content = args[0]
    else:
        content = args or kwargs
    response = BaseResponse()
    response.data = content
    return JsonExtendResponse(response)


def abort(error_code, message):
    response = BaseResponse()
    response.status = False
    response.error_code = error_code
    response.message = message
    return JsonExtendResponse(response)


def dict_to_json(data):
    if not data:
        data = {}
    return json.dumps(data, cls=JsonExtendEncoder)


def dict_to_json_ea(data=None):
    return json.dumps(data, cls=JsonExtendEncoder, ensure_ascii=False, indent=4)


def json_to_dict(json_data):
    return json.loads(json_data)
