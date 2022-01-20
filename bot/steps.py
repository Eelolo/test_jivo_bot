STEPS = {
    0: {
        'type': 'TEXT',
        'text_type': 'text',
        'text': '',
        'answers_type': 'list',
        'answers': [],
        'cases': [{
            'condition_type': 'any_text',
            'condition': '',
            'next_step': 1,
            'call_agent': False,
            'process_answer': False
        }],
    },
    1: {
        'type': 'BUTTONS',
        'text_type': 'text',
        'text': 'Здравствуйте! Позвольте помочь вам определиться с выбором продукта.',
        'answers_type': 'list',
        'answers': ['Да, пожалуйста.', 'Нет, спасибо.'],
        'cases': [{
            'condition_type': 'text',
            'condition': 'Да, пожалуйста.',
            'next_step': 0,
            'call_agent': False,
            'process_answer': True
        },
        {
            'condition_type': 'text',
            'condition': 'Нет, спасибо.',
            'next_step': 0,
            'call_agent': False,
            'process_answer': False
        }],
    },
    11: {
        'type': 'BUTTONS',
        'text_type': 'text',
        'text': 'Выберите направление продукта, которое вас интересует:',
        'answers_type': 'function',
        'answers': 'get_categories',
        'cases': [{
            'condition_type': 'function',
            'condition': 'get_categories',
            'next_step': 20,
            'call_agent': False,
            'process_answer': True
        }],
    },
    12: {
        'type': 'BUTTONS',
        'text_type': 'text',
        'text': 'Хотите выбрать еще одно направление?',
        'answers_type': 'function',
        'answers': 'get_categories',
        'cases': [{
            'condition_type': 'function',
            'condition': 'get_categories',
            'next_step': 20,
            'call_agent': False,
            'process_answer': True
        },
        {
           'condition_type': 'text',
           'condition': 'Нет, спасибо.',
           'next_step': 20,
           'call_agent': False,
           'process_answer': True
        }],
    },
    20: {
        'type': 'BUTTONS',
        'text_type': 'text',
        'text': 'Выберите отрасль применения продукта, которая вас интересует:',
        'answers_type': 'function',
        'answers': 'get_categories',
        'cases': [{
            'condition_type': 'function',
            'condition': 'get_categories',
            'next_step': 40,
            'call_agent': False,
            'process_answer': True
        },
        {
           'condition_type': 'text',
           'condition': 'Нет, спасибо.',
           'next_step': 20,
           'call_agent': False,
           'process_answer': True
        }],
    },
    40: {
        'type': 'BUTTONS',
        'text_type': 'text',
        'text': 'Хотите выбрать еще одну отрасль применения?',
        'answers_type': 'function',
        'answers': 'get_calc_purposes',
        'cases': [{
            'condition_type': 'function',
            'condition': 'get_calc_purposes_dry',
            'next_step': 50,
            'call_agent': False,
            'process_answer': True
        }],
     }
}

# 'greetings': 'Здраствуйте!',
# 'offer_to_help': 'Позвольте помочь вам определиться с выбором продукта.',
# 'parting': 'Всего доброго! Я подожду здесь. Всегда буду рад помочь.',
# 'offer_to_choose_direction': 'Выберите направление продукта, которое вас интересуют:',
# 'offer_to_choose_more_directions': 'Хотите выбрать еще одно направление?',
# 'offer_to_choose_branch_of_application': 'Выберите отрасль применения продукта, которая вас интересуют:',
# 'offer_to_choose_more_branches_of_application': 'Хотите выбрать еще одну отрасль применения?',
# 'sending_products': 'Продукты подходящие к выбранным категориям:\n',
# 'offer_to_find_related_courses': 'Хотите посмотреть учебные курсы по найденным продуктам?',
# 'sending_courses': 'Курсы по найденным продуктам:\n',
