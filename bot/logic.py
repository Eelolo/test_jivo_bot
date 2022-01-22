from bot.utils import get_or_create_instances
from bot.old_steps import STEPS
from .utils import bot_chat_logging, get_timestamp
import requests
import bot.utils as utils


class Bot:
    def __init__(self, data):
        self.event_id = data.get('id', False)
        self.client_id = data.get('client_id', False)
        self.chat_id = data.get('chat_id', False)
        self.message_text = data['message']['text'] if data.get('message', False) and data['message'].get('text', False) else ''
        self.chat, self.client = get_or_create_instances(self.chat_id, self.client_id)

        self.process_step()
        # not_understand_message(id, client_id, utime, chat)
        # invite_step(id, client_id, chat_id, utime, chat)

    def process_step(self):
        step = STEPS[self.chat.status]

        for idx, case in enumerate(step['client_answer_cases']):
            if case['func_with_condition'](self.message_text):
                self.chat.status = case['next_step']
                self.chat.save()
                self.process_answer(self.chat.status, case)
                # if STEPS[self.chat.status]['client_answer_cases'][idx]['next_step_without_client_answer']:
                #     self.process_step()
                if STEPS[case['next_step']]['client_answer_cases'][0]['next_step_without_client_answer']:
                    self.process_step()
                break

    # @bot_chat_logging
    def process_answer(self, step, case):
        if case['run_function']:
            getattr(utils, case['run_function'])(
                event_id=self.event_id,
                chat_id=self.chat_id,
                client_id=self.client_id,
                message_text=self.message_text,
                step=step, case=case
            )

        if STEPS[step]['bot_answer_type'] == 'BUTTONS':
            self.send_buttons_message(step, case)
        else:
            self.send_text_message(step, case)

    # @bot_chat_logging
    def send_text_message(self, step, case):
        payload = {
            'event': "BOT_MESSAGE",
            'id': self.event_id,
            'client_id': self.client_id,
            'message': {
                'type': "TEXT",
                'text': STEPS[step]['bot_answer_text'],
                'timestamp': get_timestamp(),
            },
        }

        if hasattr(utils, STEPS[step]['bot_answer_text']):
            payload['message']['text'] = getattr(utils, STEPS[step]['bot_answer_text'])(
                event_id=self.event_id,
                chat_id=self.chat_id,
                client_id=self.client_id,
                message_text=self.message_text,
                step=step, case=case
            )

        requests.post(
            'https://bot.jivosite.com/webhooks/dFYp2pkeg9lMsRQ/n1G0JfmBvjnXyjA',
            json=payload
        )

    # @bot_chat_logging
    def send_buttons_message(self, step, case):
        payload = {
            'event': "BOT_MESSAGE",
            'id': self.event_id,
            'client_id': self.client_id,
            'message': {
                'type': "BUTTONS",
                'title': STEPS[step]['bot_answer_text'],
                'buttons': [],
                'timestamp': get_timestamp(),
            },
        }

        buttons_text = STEPS[step]['buttons']
        if isinstance(STEPS[step]['buttons'], str) and hasattr(utils, STEPS[step]['buttons']):
            buttons_text = getattr(utils, STEPS[step]['buttons'])(
                event_id=self.event_id,
                chat_id=self.chat_id,
                client_id=self.client_id,
                message_text=self.message_text,
                step=step, case=case
            )

        for button_text in buttons_text:
            payload['message']['buttons'].append({'text': button_text})

        requests.post(
            'https://bot.jivosite.com/webhooks/dFYp2pkeg9lMsRQ/n1G0JfmBvjnXyjA',
            json=payload
        )
