from bot.utils import get_or_create_instances
from bot.utils import get_timestamp
from bot.models import Message

import requests


class Bot:
    def __init__(self, data, first_step, steps):
        print(data)
        self.event_id = data.get('id', False)
        self.client_id = data.get('client_id', False)
        self.chat_id = data.get('chat_id', False)

        if data.get('message', False) and data['message'].get('text', False):
            self.message_text = data['message']['text']
        else:
            self.message_text = ''

        self.chat, self.client = get_or_create_instances(self.chat_id, self.client_id)
        if not self.chat.step:
            self.chat.step = first_step
            self.chat.save()

        self.kwargs = {
            'event_id': self.event_id,
            'chat_id': self.chat_id,
            'client_id': self.client_id,
            'message_text': self.message_text,
        }

        self.steps = steps
        self.step = self.steps[self.chat.step](**self.kwargs)

        self.process_step()

    def client_chat_logging(func):
        def wrapper(bot):
            func(bot)
            Message.objects.create(
                client_id=bot.client, chat_id=bot.chat.pk,
                text=bot.message_text, bot=False
            )

        return wrapper

    def bot_chat_logging(func):
        def wrapper(bot):
            func(bot)
            Message.objects.create(
                client_id=bot.client, chat_id=bot.chat.pk,
                text=bot.message_text, bot=True
            )

        return wrapper

    @client_chat_logging
    def process_step(self):
        for case in self.step.client_answer_cases:
            case = case(self.message_text)

            if case:
                self.chat.step = case['next_step']
                self.chat.save()
                self.step = self.steps[self.chat.step](**self.kwargs)
                self.process_answer()

                if case['right_away']:
                    self.process_step()
                break

    @bot_chat_logging
    def process_answer(self):
        payload = {
            'event': "BOT_MESSAGE",
            'id': self.event_id,
            'client_id': self.client_id,
            'message': {
                'type': "TEXT",
                'text': self.step.answer_text,
                'timestamp': get_timestamp(),
            },
        }

        if self.step.send_buttons:
            payload['message']['type'] = 'BUTTONS'
            payload['message']['title'] = payload['message'].pop('text')
            payload['message']['buttons'] = []

            for button_text in self.step.buttons:
                payload['message']['buttons'].append({'text': button_text})

        self.send_message(payload)

    def send_message(self, payload):
        requests.post(
            'https://bot.jivosite.com/webhooks/dFYp2pkeg9lMsRQ/n1G0JfmBvjnXyjA',
            json=payload
        )
