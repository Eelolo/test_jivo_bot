import json
from copy import copy
import requests

from qualificator.bot import utils, steps
from steps import process_answer
from qualificator.models import FormResult


def process_callback(request):
    _body = request.body.decode("utf-8")
    jivo_data = json.loads(_body)

    id = jivo_data.get('id', False)
    client_id = jivo_data.get('client_id', False)
    chat_id = jivo_data.get('chat_id', False)

    response = {}
    if not id:
        response['error'] = {'code': 1, 'message': 'No id'}
    elif not client_id:
        response['error'] = {'code': 2, 'message': 'No client id'}
    elif not chat_id:
        response['error'] = {'code': 3, 'message': 'No chat_id'}

    if not response:
        return jivo_data, id, client_id, chat_id

    return response


def get_finalized_step_text(step, chat):
    try:
        step = steps.STEPS[step]
        if step['text_type'] == 'text':
            _text = step['text']
        elif step['text_type'] == 'function':
            _text = steps.get_step_text(chat)
        else:
            _text = '?Что-то пошло не так?'
        return _text
    except KeyError:
        return '?Нет такого шага?'
    except:
        raise


def invite_step(id, client_id, chat_id, utime, chat):
    try:
        step = steps.STEPS[chat.step]
    except KeyError:
        return
    except:
        raise

    if step['text_type'] == 'text':
        _text = step['text']
    elif step['text_type'] == 'function':
        _text = steps.get_step_text(chat)
    else:
        _text = 'Что-то пошло не так!!!'

    if step['type'] == 'TEXT':
        data = {
            'event': 'BOT_MESSAGE',
            'id': id,
            'client_id': client_id,
            'chat_id': chat_id,
            'message': {
                'type': step['type'],
                'text': _text,
                'timestamp': utime,
            }
        }
    elif step['type'] == 'BUTTONS':
        if step['answers_type'] == 'list':
            _answers = [{'text': answer} for answer in step['answers']]
        elif step['answers_type'] == 'function':
            _answers = getattr(utils, step['answers'])()
        else:
            _answers = [{'text': 'Что-то пошло не так!!!'}]

        data = {
            'event': 'BOT_MESSAGE',
            'id': id,
            'client_id': client_id,
            'chat_id': chat_id,
            'message': {
                'type': step['type'],
                'title': _text,
                'text': _text,
                'buttons': _answers,
                'timestamp': utime,
            }
        }
    else:
        data = {
            'event': 'BOT_MESSAGE',
            'id': id,
            'client_id': client_id,
            'chat_id': chat_id,
            'message': {
                'type': 'TEXT',
                'text': 'Что-то пошло не так!!!',
                'timestamp': utime,
            },
        }

    req = requests.post(
        'https://bot.jivosite.com/webhooks/yYZ5SGhl1ZnbfW9/d7Vum8EyXXwch0TqMfJv0NgfsdAM1MZPixqwYoGW',
        json=data
    )


def process_step(id, client_id, chat_id, text, chat):
    try:
        step = steps.STEPS[chat.step]
    except KeyError:
        return chat
    except:
        raise

    succeed = False
    old_step = copy(chat.step)

    for case in step['cases']:
        if succeed:
            break
        if case['condition_type'] == 'list':
            if text.lower() in [x.lower() for x in case['condition']]:
                chat.step = case['next_step']
                chat.agent_flags = case['agent_flags']
                chat.save()
                succeed = True
        elif case['condition_type'] == 'text':
            if text.lower() == case['condition'].lower():
                chat.step = case['next_step']
                chat.agent_flags = case['agent_flags']
                chat.save()
                succeed = True
        elif case['condition_type'] == 'function':
            func = getattr(utils, case['condition'])
            answers = func()
            if text.lower() in [x.lower() for x in answers]:
                chat.step = case['next_step']
                chat.agent_flags = case['agent_flags']
                chat.save()
                succeed = True
        elif case['condition_type'] == 'any_text':
            chat.step = case['next_step']
            chat.agent_flags = case['agent_flags']
            chat.save()
            succeed = True

        if case['process_answer'] and succeed:
            process_answer(old_step, chat, chat_id, text)

        if case['call_agent'] and succeed:
            call_agent(id, client_id, chat_id)

        if not succeed:
            chat.agent_flags += 1

    return chat