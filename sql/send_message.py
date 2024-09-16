import httpx
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live

console = Console(width=100)


def fetch_stream(access_token, content, conversation_id):
    url = 'http://127.0.0.1:8848/chats/send-message'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {
        'content': content,
        'conversation_id': conversation_id
    }
    s = []
    with httpx.Client() as client:
        with client.stream('POST', url, json=data, headers=headers) as response:
            for line in response.iter_raw():
                ret = line.decode('utf-8')
                if ret.endswith('\n'):
                    ret = ret[:-1]
                s.append(ret)
                yield ret


def run(access_token, content, conversation_id):
    output_buffer = ''
    with Live(console=console, refresh_per_second=4) as live:
        for chunk in fetch_stream(access_token, content, conversation_id):
            output_buffer += chunk
            md = Markdown(output_buffer)
            live.update(md)


if __name__ == '__main__':
    access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxNzI2NTgzMTkxLjI1OTc4N30.umyVOAZqtTZeUeCctCFT7Rm0QDCu05U1Uj_fAUOVF2s'
    conversation_id = 'b56e1308378b44248a7c9e011d1cdbad'
    content = '你是谁？'
    run(access_token, content, conversation_id)
