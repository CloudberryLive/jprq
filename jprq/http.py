import base64
import json
import bson
from urllib.parse import urljoin

import aiohttp


class Client:
    def __init__(self, base_uri, token):
        self.base_uri = base_uri
        self.token = token

    async def process(self, message, websocket):
        async with aiohttp.ClientSession() as session:
            try:
                response = await session.request(
                    method=message['method'],
                    url=urljoin(self.base_uri, message['url']),
                    headers=message['header'],
                    data=base64.b64decode(message['body']),
                )
            except:
                print(f"Error Processing Request At: {message['url']}")
                return {
                    'request_id': message['id'],
                    'token': self.token,
                    'status': 500,
                    'header': {},
                    'body': base64.b64encode(b'request failed').decode('utf-8'),
                }

            body = await response.read()
            header = message['header']
            header['Content-Length'] = len(body)

            response_message = {
                'request_id': message['id'],
                'token': self.token,
                'status': response.status,
                'header': header,
                'body': body.decode('utf-8'),
            }
            await websocket.send(bson.dumps(response_message))