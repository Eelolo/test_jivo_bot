from bot.utils import get_or_create_instances
from bot.models import Message
from bot.steps import STEPS
from copy import copy


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
        old_step = copy(chat.step)

        for case in step['cases']:
            if succeed:
                break
            print(case)
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
                    process_answer(old_step, chat, chat_id, text)

            # if case['call_agent'] and succeed:
            #     call_agent(id, client_id, chat_id)

            # if not succeed:
            #     chat.agent_flags += 1

        return chat

    def process_answer(self, step_number, chat, chat_id, text):
        from qualificator.bot.logics import get_or_create_qualificator_instance

        if step_number == 11 or step_number == 2011:
            chat = get_or_create_qualificator_instance(chat, chat_id)
            chat.form_result.industry_focus.set(IndustryFocus.objects.filter(title__icontains=text))
            chat.form_result.save()
        if step_number == 12 or step_number == 2012:
            chat = get_or_create_qualificator_instance(chat, chat_id)
            if text != 'Другая':
                chat.form_result.industry_focus.set(IndustryFocus.objects.filter(title__icontains=text))
            chat.form_result.save()
        if step_number == 20:
            chat.form_result.physic_task_type.set(PhysicTaskType.objects.filter(title__icontains=text))
            chat.form_result.save()
        if step_number == 40:
            chat.form_result.calculations_purpose.set(CalculationsPurpose.objects.filter(title__icontains=text))
            chat.form_result.save()
