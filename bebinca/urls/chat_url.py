from starlette.routing import Router

from bebinca.views import chat_view

chat_url = Router()

chat_url.add_route('/chat-id', chat_view.get_chat_id, ['POST'])  # 所有接口只采用 POST 方式
chat_url.add_route('/send-message', chat_view.send_message, ['POST'])
