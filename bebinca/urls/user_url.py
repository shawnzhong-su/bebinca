from starlette.routing import Router

from bebinca.views import user_view

user_url = Router()

user_url.add_route('/get-access-token', user_view.get_access_token, ['GET', 'POST'])
