from bebinca.models.user_model import UserModel
from bebinca.utils.tools import jsonify, abort
from bebinca.utils import jwt_util


async def get_access_token(request):
    body = await request.json()
    phone_number = body['phone_number']
    password = body['password']
    user_info = await UserModel().get_user_by_phone(phone_number)
    if not user_info:
        abort(403, 'account does not exist')
    db_password = user_info['PasswordHash']
    is_pwd = jwt_util.validate_password(password, db_password)
    if not is_pwd:
        abort(403, 'invalid password')
    access_token = jwt_util.generate_token({'id': user_info['ID']})
    jwt_token = {'access_token': access_token, 'token_type': 'bearer'}
    return jsonify(jwt_token)
