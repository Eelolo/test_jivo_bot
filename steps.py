STEPS = {
    0: {'type': 'TEXT',
        'text_type': 'text',
        'text': '',
        'answers_type': 'list',
        'answers': [],
        'cases': [{'condition_type': 'any_text',
                   'condition': '',
                   'next_step': 1,
                   'call_agent': False,
                   'agent_flags': 0,
                   'process_answer': False},
                  ],
        },
    1: {'type': 'BUTTONS',
        'text_type': 'text',
        'text': 'Я Цифробот и у меня есть несколько полезных навыков. Выберите, пожалуйста один из списка',
        'answers_type': 'list',
        'answers': ['Оценить срок и стоимость', 'Подобрать информацию', 'Связаться со специалистом'],
        'cases': [{'condition_type': 'text',
                   'condition': 'Оценить срок и стоимость',
                   'next_step': 11,
                   'call_agent': False,
                   'agent_flags': 0,
                   'process_answer': False},
                  {'condition_type': 'text',
                   'condition': 'Подобрать информацию',
                   'next_step': 2011,
                   'call_agent': False,
                   'agent_flags': 0,
                   'process_answer': False},
                  {'condition_type': 'text',
                   'condition': 'Связаться со специалистом',
                   'next_step': 1101,
                   'call_agent': False,
                   'agent_flags': 0,
                   'process_answer': False}
                  ],
        },
    11: {'type': 'BUTTONS',
         'text_type': 'text',
         'text': 'К какой отрасли промышленности относится Ваша задача?',
         'answers_type': 'function',
         'answers': 'get_industries_featured',
         'cases': [{'condition_type': 'function',
                    'condition': 'get_industries_featured_dry',
                    'next_step': 20,
                    'call_agent': False,
                    'agent_flags': 0,
                    'process_answer': True},
                   {'condition_type': 'text',
                    'condition': 'Другая',
                    'next_step': 12,
                    'call_agent': False,
                    'agent_flags': 0,
                    'process_answer': False}],
         },
    12: {'type': 'BUTTONS',
         'text_type': 'text',
         'text': 'Может быть подойдет что-то из этого списка?',
         'answers_type': 'function',
         'answers': 'get_industries_not_featured',
         'cases': [{'condition_type': 'function',
                    'condition': 'get_industries_not_featured_dry',
                    'next_step': 20,
                    'call_agent': False,
                    'agent_flags': 0,
                    'process_answer': True},
                   {'condition_type': 'text',
                    'condition': 'Другая',
                    'next_step': 20,
                    'call_agent': False,
                    'agent_flags': 0,
                    'process_answer': True}],
         },
    20: {'type': 'BUTTONS',
         'text_type': 'text',
         'text': 'К какой области физики относится Ваша задача?',
         'answers_type': 'function',
         'answers': 'get_physics',
         'cases': [{'condition_type': 'function',
                    'condition': 'get_physics_dry',
                    'next_step': 40,
                    'call_agent': False,
                    'agent_flags': 0,
                    'process_answer': True}],
         },
    40: {'type': 'BUTTONS',
         'text_type': 'text',
         'text': 'Пожалуйста, укажите цель выполнения расчетов:',
         'answers_type': 'function',
         'answers': 'get_calc_purposes',
         'cases': [{'condition_type': 'function',
                    'condition': 'get_calc_purposes_dry',
                    'next_step': 50,
                    'call_agent': False,
                    'agent_flags': 0,
                    'process_answer': True}],
         },

def process_answer(step_number, chat, chat_id, text):
    from logics import get_or_create_qualificator_instance

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


STEPS = {
    0: {'type': 'TEXT',
        'text_type': 'text',
        'text': '',
        'answers_type': 'list',
        'answers': [],
        'cases': [{'condition_type': 'any_text',
                   'condition': '',
                   'next_step': 1,
                   'call_agent': False,
                   'agent_flags': 0,
                   'process_answer': False},
                  ],
        },
    1: {'type': 'BUTTONS',
        'text_type': 'text',
        'text': 'Я Цифробот и у меня есть несколько полезных навыков. Выберите, пожалуйста один из списка',
        'answers_type': 'list',
        'answers': ['Оценить срок и стоимость', 'Подобрать информацию', 'Связаться со специалистом'],
        'cases': [{'condition_type': 'text',
                   'condition': 'Оценить срок и стоимость',
                   'next_step': 11,
                   'call_agent': False,
                   'agent_flags': 0,
                   'process_answer': False},
                  {'condition_type': 'text',
                   'condition': 'Подобрать информацию',
                   'next_step': 2011,
                   'call_agent': False,
                   'agent_flags': 0,
                   'process_answer': False},
                  {'condition_type': 'text',
                   'condition': 'Связаться со специалистом',
                   'next_step': 1101,
                   'call_agent': False,
                   'agent_flags': 0,
                   'process_answer': False}
                  ],
        },
    11: {'type': 'BUTTONS',
         'text_type': 'text',
         'text': 'К какой отрасли промышленности относится Ваша задача?',
         'answers_type': 'function',
         'answers': 'get_industries_featured',
         'cases': [{'condition_type': 'function',
                    'condition': 'get_industries_featured_dry',
                    'next_step': 20,
                    'call_agent': False,
                    'agent_flags': 0,
                    'process_answer': True},
                   {'condition_type': 'text',
                    'condition': 'Другая',
                    'next_step': 12,
                    'call_agent': False,
                    'agent_flags': 0,
                    'process_answer': False}],
         },
    12: {'type': 'BUTTONS',
         'text_type': 'text',
         'text': 'Может быть подойдет что-то из этого списка?',
         'answers_type': 'function',
         'answers': 'get_industries_not_featured',
         'cases': [{'condition_type': 'function',
                    'condition': 'get_industries_not_featured_dry',
                    'next_step': 20,
                    'call_agent': False,
                    'agent_flags': 0,
                    'process_answer': True},
                   {'condition_type': 'text',
                    'condition': 'Другая',
                    'next_step': 20,
                    'call_agent': False,
                    'agent_flags': 0,
                    'process_answer': True}],
         },
    20: {'type': 'BUTTONS',
         'text_type': 'text',
         'text': 'К какой области физики относится Ваша задача?',
         'answers_type': 'function',
         'answers': 'get_physics',
         'cases': [{'condition_type': 'function',
                    'condition': 'get_physics_dry',
                    'next_step': 40,
                    'call_agent': False,
                    'agent_flags': 0,
                    'process_answer': True}],
         },
    40: {'type': 'BUTTONS',
         'text_type': 'text',
         'text': 'Пожалуйста, укажите цель выполнения расчетов:',
         'answers_type': 'function',
         'answers': 'get_calc_purposes',
         'cases': [{'condition_type': 'function',
                    'condition': 'get_calc_purposes_dry',
                    'next_step': 50,
                    'call_agent': False,
                    'agent_flags': 0,
                    'process_answer': True}],
         },

def process_answer(step_number, chat, chat_id, text):
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

def get_step_text(chat):
    text = 'Что-то пошло не так!!!'
    if chat.step == 72:
        tasks = PhysicTask.objects.filter(featured=True, task_level__title='Специализированная',
                                          physic_type=chat.form_result.physic_task_type.all().first())
        tasks_text = ', '.join([t.title for t in tasks])
        text = f'Соответствует ли вашей задаче какая то из перечисленных в этом списке: {tasks_text}?'
    if chat.step == 73:
        tasks = PhysicTask.objects.filter(featured=True, task_level__title='Уникальная',
                                          physic_type=chat.form_result.physic_task_type.all().first())
        tasks_text = ', '.join([t.title for t in tasks])
        text = f'Соответствует ли вашей задаче какая то из перечисленных в этом списке: {tasks_text}?'
    if chat.step == 1000:
        text = f'Спасибо за обращение! Срок решения вашей задачи от {chat.form_result.days} дней. ' \
               f'Стоимость решения задачи от {int(chat.form_result.price)} рублей. ' \
               f'Хотите оставить свои данные, чтобы с Вами связался наш специалист?'
    if chat.step == 2020:
        _tag_page = f'https://multiphysics.ru/tags/{chat.form_result.industry_focus.all().first().related_site_tag}.htm'
        _site_page = f'https://multiphysics.ru/otrasli/{chat.form_result.industry_focus.all().first().related_site_page}.htm'
        text = f'О нашем опыте и выполненных проектах вы можете узнать на страницах: {_site_page} и {_tag_page} ' \
               f'Кстати, стоимость решения задач для этой отрасли начинается от {int(chat.form_result.price)} рублей. ' \
               f'Хотите более точно оценить стоимость и срок решения Вашей задачи?'
    if chat.step == 2021:
        _tag_page = f'https://multiphysics.ru/tags/{chat.form_result.industry_focus.all().first().related_site_tag}.htm'
        _site_page = f'https://multiphysics.ru/otrasli/{chat.form_result.industry_focus.all().first().related_site_page}.htm'
        text = f'О нашем опыте и выполненных проектах вы можете узнать на страницах: {_site_page} и {_tag_page} ' \
               f'Начать сначала?'
    return text