import time

import httpx
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live

console = Console(width=100)


def fetch_stream(content, conversation_id):
    url = 'http://127.0.0.1:8848/chats/send-message'
    s = []
    with httpx.Client() as client:
        with client.stream('POST', url, json={'content': content, 'conversation_id': conversation_id}) as response:
            for line in response.iter_raw():
                ret = line.decode('utf-8')
                if ret.endswith('\n'):
                    ret = ret[:-1]
                s.append(ret)
                yield ret


def run(content, conversation_id):
    output_buffer = ''
    with Live(console=console, refresh_per_second=4) as live:
        for chunk in fetch_stream(content, conversation_id):
            output_buffer += chunk
            md = Markdown(output_buffer)
            live.update(md)


if __name__ == '__main__':
    conversation_id = '7e6f85c0439d4b98b3297e233420cec4'
    content = 'flask框架为什么没有starletter框架的api对程序员友好？'
    run(content, conversation_id)
