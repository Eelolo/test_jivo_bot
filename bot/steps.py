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
import bot.utils as utils


STEPS = {
    0: {
        'bot_answer_type': 'TEXT',
        'bot_answer_text': '',
        'client_answer_cases': [{
            'func_with_condition': lambda string: True,
            'client_answer': '',
            'next_step': 1,
            'next_step_without_client_answer': False,
            'run_function': ''
        }],
    },
    1: {
        'bot_answer_type': 'BUTTONS',
        'bot_answer_text': 'Здравствуйте! Позвольте помочь вам определиться с выбором продукта.',
        'buttons': ['Да, пожалуйста.', 'Нет, спасибо.'],
        'client_answer_cases': [{
            'func_with_condition': lambda string: string == 'Да, пожалуйста.',
            'client_answer': 'Да, пожалуйста.',
            'next_step': 11,
            'next_step_without_client_answer': False,
            'run_function': ''
        },
        {
            'func_with_condition': lambda string: string == 'Нет, спасибо.',
            'client_answer': 'Нет, спасибо.',
            'next_step': 2,
            'next_step_without_client_answer': False,
            'run_function': ''
        }],
    },
    2: {
        'bot_answer_type': 'TEXT',
        'bot_answer_text': 'Всего доброго! Я подожду здесь. Всегда буду рад помочь.',
        'client_answer_cases': [{
            'func_with_condition': lambda string: True,
            'client_answer': '',
            'next_step': 1,
            'next_step_without_client_answer': False,
            'run_function': ''
        }]
    },
    11: {
        'bot_answer_type': 'BUTTONS',
        'bot_answer_text': 'Выберите направление продукта, которое вас интересует:',
        'buttons': 'get_directions',
        'client_answer_cases': [{
            'func_with_condition': lambda string: string in getattr(utils, 'get_directions')(),
            'client_answer': '',
            'next_step': 21,
            'next_step_without_client_answer': False,
            'run_function': 'add_to_selected_categories'
        }],
    },
    21: {
        'bot_answer_type': 'BUTTONS',
        'bot_answer_text': 'Хотите выбрать еще одно направление?',
        'buttons': ['Да, пожалуйста.', 'Нет, спасибо.'],
        'client_answer_cases': [{
            'func_with_condition': lambda string: string == 'Да, пожалуйста.',
            'client_answer': 'Да, пожалуйста.',
            'next_step': 11,
            'next_step_without_client_answer': False,
            'run_function': ''
        },
        {
            'func_with_condition': lambda string: string == 'Нет, спасибо.',
            'client_answer': 'Нет, спасибо.',
            'next_step': 31,
            'next_step_without_client_answer': False,
            'run_function': ''
        }],
    },
    31: {
        'bot_answer_type': 'BUTTONS',
        'bot_answer_text': 'Выберите отрасль применения продукта, которая вас интересуют:',
        'buttons': 'get_branches_of_application',
        'client_answer_cases': [{
            'func_with_condition': lambda string: string in getattr(utils, 'get_branches_of_application')(),
            'client_answer': '',
            'next_step': 41,
            'next_step_without_client_answer': False,
            'run_function': 'add_to_selected_categories'
        }],
    },
    41: {
        'bot_answer_type': 'BUTTONS',
        'bot_answer_text': 'Хотите выбрать еще одну отрасль применения?',
        'buttons': ['Да, пожалуйста.', 'Нет, спасибо.'],
        'client_answer_cases': [{
            'func_with_condition': lambda string: string == 'Да, пожалуйста.',
            'client_answer': 'Да, пожалуйста.',
            'next_step': 31,
            'next_step_without_client_answer': False,
            'run_function': ''
        },
        {
            'func_with_condition': lambda string: string == 'Нет, спасибо.',
            'client_answer': 'Нет, спасибо.',
            'next_step': 51,
            'next_step_without_client_answer': False,
            'run_function': ''
        }],
    },
    51: {
        'bot_answer_type': 'TEXT',
        'bot_answer_text': 'get_products_from_categories_text',
        'client_answer_cases': [{
            'func_with_condition': lambda string: True,
            'client_answer': '',
            'next_step': 61,
            'next_step_without_client_answer': True,
            'run_function': ''
        }]
    },
    61: {
        'bot_answer_type': 'BUTTONS',
        'bot_answer_text': 'Хотите посмотреть учебные курсы по найденным продуктам?',
        'buttons': ['Да, пожалуйста.', 'Нет, спасибо.'],
        'client_answer_cases': [{
            'func_with_condition': lambda string: string == 'Да, пожалуйста.',
            'client_answer': 'Да, пожалуйста.',
            'next_step': 71,
            'next_step_without_client_answer': False,
            'run_function': ''
        },
        {
            'func_with_condition': lambda string: string == 'Нет, спасибо.',
            'client_answer': 'Нет, спасибо.',
            'next_step': 2,
            'next_step_without_client_answer': False,
            'run_function': ''
        }],
    },
    71: {
        'bot_answer_type': 'TEXT',
        'bot_answer_text': 'get_related_courses',
        'client_answer_cases': [{
            'func_with_condition': lambda string: True,
            'client_answer': '',
            'next_step': 2,
            'next_step_without_client_answer': True,
            'run_function': ''
        }]
    }
}
