import httpx


def get_chat_id(access_token, title):
    url = 'http://127.0.0.1:8848/chats/chat-id'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {'title': title}
    with httpx.Client() as client:
        response = client.post(url, json=data, headers=headers)
        data = response.json()
        chat_id = data['data']
        return chat_id


if __name__ == '__main__':
    access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxNzI2NTgzMTkxLjI1OTc4N30.umyVOAZqtTZeUeCctCFT7Rm0QDCu05U1Uj_fAUOVF2s'
    title = '你是谁？'
    print(get_chat_id(access_token, title))
