import random
import json
import uuid
import time
import requests
from config import config
from comon_functions.lprint import lprint


class GigaChat:
    URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    RESP_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    token = None
    callback_func = None
    _messages = {}

    @classmethod
    def make_gigachat_request(cls, model, messages, max_tokens, top_p, frequency_penalty):
        response_message = F"Внутрення ошибка сервера {random.random()}"
        try:
            lprint.p("try GigaChat request")
            if cls.token is None or cls.token['expires_at'] < int(time.time() * 1000):
                payload = 'scope=GIGACHAT_API_PERS'
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'application/json',
                    'RqUID': str(uuid.uuid4()),
                    'Authorization': F'Basic {config.GIGACHAT_AUTH_DATA}'
                }
                response = requests.post(cls.URL,
                                         headers=headers,
                                         data=payload,
                                         verify=False,
                                         timeout=120)
                cls.token = response.json()
            response_message = ""
            payload = json.dumps({
                "model": model,
                "messages": messages,
                "stream": False,
                "repetition_penalty": frequency_penalty,
                "max_tokens": max_tokens,
                "top_p": top_p,
            })
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': F'Bearer {cls.token["access_token"]}'
            }
            response = requests.post(cls.RESP_URL,
                                     headers=headers,
                                     data=payload,
                                     verify=False,
                                     timeout=120)
            response = response.json()
            response_message = response['choices'][0]['message']['content']
            lprint.p("request completed", response['usage'])
        except Exception as e:
            lprint.p("Error request to gigachad ", e, response.json())
            return {"status": "error", "message": e}

        return {"status": "ok", "message": response_message}

    @classmethod
    def purge_user_messages(cls, user_id):
        if len(cls._messages[user_id]) > 30:
            cls._messages[user_id].pop(0)

    @classmethod
    def add_message(cls, user_id, role, message, ai_prompt, response_callback):
        cls.callback_func = response_callback
        if user_id not in cls._messages:
            cls._messages[user_id] = []
        the_message = {'role': role, 'message': message}
        cls._messages[user_id].append(the_message)
        cls.purge_user_messages(user_id)
        if role == 'user':
            cls.ai_process_message(user_id, ai_prompt)

    @classmethod
    def ai_process_message(cls, user_id, ai_prompt):
        messages = [{"role": "system", "content": ai_prompt}]
        for message in cls._messages[user_id]:
            current_message = {}
            current_message['role'] = 'assistant' if message['role'] == 'bot' else 'user'
            current_message['content'] = message['message']
            messages.append(current_message)
        resp = GigaChat.make_gigachat_request(model="GigaChat",
                                              messages=messages,
                                              max_tokens=999,
                                              top_p=0.75,
                                              frequency_penalty=1.0)
        if resp["status"] == "ok":
            cls.add_message(user_id, 'bot', resp['message'], ai_prompt, cls.callback_func)
            cls.callback_func(user_id, resp['message'])
