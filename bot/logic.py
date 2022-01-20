from bot.utils import get_or_create_instances
from bot.models import Message
from bot.steps import STEPS
from copy import copy
from .utils import bot_chat_logging, get_timestamp
import requests


class Bot:
    def __init__(self, data):
        id = data.get('id', False)
        client_id = data.get('client_id', False)
        chat_id = data.get('chat_id', False)
        text = ''

        chat, chat_client = get_or_create_instances(chat_id, client_id)

        if data.get('message', False) and data['message'].get('text', False):
            text = data['message']['text']

        chat = self.process_step(id, client_id, chat_id, text, chat)
        # not_understand_message(id, client_id, utime, chat)
        # invite_step(id, client_id, chat_id, utime, chat)

    def process_step(self, id, client_id, chat_id, text, chat):
        try:
            step = STEPS[chat.status]
        except KeyError:
            return chat
        except:
            raise

        succeed = False
        old_step = copy(chat.status)

        for case in step['cases']:
            if succeed:
                break
            if case['condition_type'] == 'list' and text.lower() in [x.lower() for x in case['condition']] \
                or case['condition_type'] == 'text' and text.lower() == case['condition'].lower() \
                or case['condition_type'] == 'function' \
                or case['condition_type'] == 'any_text':

                if case['condition_type'] == 'function':
                    func = getattr(utils, case['condition'])
                    answers = func()
                    if text.lower() in [x.lower() for x in answers]:
                        succeed = True
                else:
                    succeed = True

            if succeed:
                chat.status = case['next_step']
                # chat.agent_flags = 0
                chat.save()
                if case['process_answer']:
                    self.process_answer(old_step, id, client_id)

            # if case['call_agent'] and succeed:
            #     call_agent(id, client_id, chat_id)

            # if not succeed:
            #     chat.agent_flags += 1

        return chat

    # @bot_chat_logging
    def process_answer(self, step_number, id, client_id):
        payload = {
            'event': "BOT_MESSAGE",
            'id': id,
            'client_id': client_id,
            'message': {
                'type': "BUTTONS",
                'title': STEPS[step_number]['text'],
                'buttons': [],
                'timestamp': get_timestamp(),
            },
        }

        for text in STEPS[step_number]['answers']:
            payload['message']['buttons'].append({'text': text})

        requests.post(
            'https://bot.jivosite.com/webhooks/dFYp2pkeg9lMsRQ/n1G0JfmBvjnXyjA',
            json=payload
        )