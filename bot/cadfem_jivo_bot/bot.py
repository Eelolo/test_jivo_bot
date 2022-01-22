from bot.utils import get_or_create_instances
from bot.old_steps import STEPS
from bot.utils import bot_chat_logging, get_timestamp
import requests
from bot.models import Chat

class Bot:
    def __init__(self, data, steps):
        self.event_id = data.get('id', False)
        self.client_id = data.get('client_id', False)
        self.chat_id = data.get('chat_id', False)
        self.message_text = data['message']['text'] if data.get('message', False) and data['message'].get('text', False) else ''
        self.chat, self.client = get_or_create_instances(self.chat_id, self.client_id)
        self.steps = steps
        self.kwargs = {
            'event_id': self.event_id,
            'chat_id': self.chat_id,
            'client_id': self.client_id,
            'message_text': self.message_text,
        }
        self.process_step()

    def process_step(self):
        step = self.steps[self.chat.step](**self.kwargs)
        print(f'step from db: {step}')

        for case in step.client_answer_cases:
            case = case(self.message_text)
            if case:
                self.chat.step = case['next_step']
                print(f'saved in db: {case["next_step"]}')
                self.chat.save()
                self.chat = Chat.objects.get(chat_id=self.chat_id)
                step = self.steps[self.chat.step](**self.kwargs)
                print(f'new step: {step}')
                # self.process_answer(step)
                if case['right_away']:
                    self.process_step()
                break

    # @bot_chat_logging
    def process_answer(self, step):
        if step.send_buttons:
            self.send_buttons_message(step)
        else:
            self.send_text_message(step)

    # @bot_chat_logging
    def send_text_message(self, step):
        payload = {
            'event': "BOT_MESSAGE",
            'id': self.event_id,
            'client_id': self.client_id,
            'message': {
                'type': "TEXT",
                'text': step.answer_text,
                'timestamp': get_timestamp(),
            },
        }

        r = requests.post(
            'https://bot.jivosite.com/webhooks/dFYp2pkeg9lMsRQ/n1G0JfmBvjnXyjA',
            json=payload
        )

        print('from text msg', r.content)

    # @bot_chat_logging
    def send_buttons_message(self, step):
        payload = {
            'event': "BOT_MESSAGE",
            'id': self.event_id,
            'client_id': self.client_id,
            'message': {
                'type': "BUTTONS",
                'title': step.answer_text,
                'buttons': [],
                'timestamp': get_timestamp(),
            },
        }

        for button_text in step.buttons:
            payload['message']['buttons'].append({'text': button_text})

        r = requests.post(
            'https://bot.jivosite.com/webhooks/dFYp2pkeg9lMsRQ/n1G0JfmBvjnXyjA',
            json=payload
        )

        print('from btn msg', r.content)