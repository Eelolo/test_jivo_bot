# STEPS = {
#     0: {
#         'bot_answer_type': 'TEXT',
#         'bot_answer_text': '',
#         'client_answer_cases': [{
#             'func_with_condition': lambda string: True,
#             'client_answer': '',
#             'next_step': 1,
#             'next_step_without_client_answer': False,
#             'run_function': ''
#         }],
#     },
#
# }
from bot.cadfem_jivo_bot.steps import Step
from bot.utils import (
    get_directions, get_branches_of_application, add_to_selected_categories,
    get_products_from_categories_text, get_related_courses
)


class OfferToHelpStep(Step):
    def __init__(self):
        self.set_answer_text('Здравствуйте! Позвольте помочь вам определиться с выбором продукта.')
        self.set_send_buttons(True)
        self.set_buttons(['Да, пожалуйста.', 'Нет, спасибо.'])

        self.add_client_answer_case(self.accept)
        self.add_client_answer_case(self.decline)

    def accept(self, string, **kwargs):
        if string == 'Да, пожалуйста.':
            return {'next_step': 'OfferToChooseDirectionStep', 'right_away': False}

    def decline(self, string, **kwargs):
        if string == 'Нет, спасибо.':
            return {'next_step': 'PartingStep', 'right_away': False}


class PartingStep(Step):
    def __init__(self):
        self.set_answer_text('Всего доброго! Я подожду здесь. Всегда буду рад помочь.')

    def run_anyway(self, **kwargs):
        return {'next_step': 'OfferToHelpStep', 'right_away': False}


class OfferToChooseDirectionStep(Step):
    def __init__(self):
        self.set_answer_text('Выберите направление продукта, которое вас интересует:')
        self.set_send_buttons(True)

        self.directions = get_directions()
        self.set_buttons(self.directions)

        self.add_client_answer_case(self.selected_in_product_directions)

    def selected_in_product_directions(self, string, **kwargs):
        if string in self.directions:
            add_to_selected_categories(**kwargs)
            return {'next_step': 'OfferToChooseMoreDirectionsStep', 'right_away': False}


class OfferToChooseMoreDirectionsStep(Step):
    def __init__(self):
        self.set_answer_text('Хотите выбрать еще одно направление?')
        self.set_send_buttons(True)
        self.set_buttons(['Да, пожалуйста.', 'Нет, спасибо.'])

        self.add_client_answer_case(self.accept)
        self.add_client_answer_case(self.decline)

    def accept(self, string, **kwargs):
        if string == 'Да, пожалуйста.':
            return {'next_step': 'OfferToChooseDirectionStep', 'right_away': False}

    def decline(self, string, **kwargs):
        if string == 'Нет, спасибо.':
            return {'next_step': 'OfferToChooseBranchOfApplicationStep', 'right_away': False}


class OfferToChooseBranchOfApplicationStep(Step):
    def __init__(self):
        self.set_answer_text('Выберите отрасль применения продукта, которая вас интересует:')
        self.set_send_buttons(True)

        self.get_branches_of_application = get_branches_of_application()
        self.set_buttons(self.get_branches_of_application)

        self.add_client_answer_case(self.selected_in_product_branches_of_application)

    def selected_in_product_branches_of_application(self, string, **kwargs):
        if string in self.get_branches_of_application:
            add_to_selected_categories(**kwargs)
            return {'next_step': 'OfferToChooseMoreBranchesOfApplicationStep', 'right_away': False}


class OfferToChooseMoreBranchesOfApplicationStep(Step):
    def __init__(self):
        self.set_answer_text('Хотите выбрать еще одну отрасль применения?')
        self.set_send_buttons(True)
        self.set_buttons(['Да, пожалуйста.', 'Нет, спасибо.'])

        self.add_client_answer_case(self.accept)
        self.add_client_answer_case(self.decline)

    def accept(self, string, **kwargs):
        if string == 'Да, пожалуйста.':
            return {'next_step': 'OfferToChooseBranchOfApplicationStep', 'right_away': False}

    def decline(self, string, **kwargs):
        if string == 'Нет, спасибо.':
            return {'next_step': 'SendingProductsStep', 'right_away': False}


class SendingProductsStep(Step):
    def __init__(self):
        self.set_answer_text(get_products_from_categories_text())

        self.add_client_answer_case(self.run_anyway)

    def run_anyway(self, string, **kwargs):
        return {'next_step': 'OfferToFindRelatedCoursesStep', 'right_away': True}


class OfferToFindRelatedCoursesStep(Step):
    def __init__(self):
        self.set_answer_text('Хотите посмотреть учебные курсы по найденным продуктам?')
        self.set_send_buttons(True)
        self.set_buttons(['Да, пожалуйста.', 'Нет, спасибо.'])

        self.add_client_answer_case(self.accept)
        self.add_client_answer_case(self.decline)

    def accept(self, string, **kwargs):
        if string == 'Да, пожалуйста.':
            return {'next_step': 'SendingCoursesStep', 'right_away': False}

    def decline(self, string, **kwargs):
        if string == 'Нет, спасибо.':
            return {'next_step': 'PartingStep', 'right_away': False}


class SendingCoursesStep(Step):
    def __init__(self):
        self.set_answer_text(get_related_courses())
        self.add_client_answer_case(self.run_anyway)

    def run_anyway(self, string, **kwargs):
        return {'next_step': 'PartingStep', 'right_away': True}
