from bot.cadfem_jivo_bot.steps import Step
from bot.utils import (
    get_directions, get_branches_of_application, add_to_selected_categories,
    get_products_from_categories_text, get_related_courses
)


class OfferToHelpStep(Step):
    def __init__(self, **kwargs):
        self.set_answer_text('Здравствуйте! Позвольте помочь вам определиться с выбором продукта.')
        self.set_send_buttons(True)
        self.set_buttons(['да', 'нет'])

        self.add_client_answer_case(self.accept)
        self.add_client_answer_case(self.decline)

    def accept(self, string):
        if string == 'да':
            return {'next_step': 'OfferToChooseDirectionStep', 'right_away': False}

    def decline(self, string):
        if string == 'нет':
            return {'next_step': 'PartingStep', 'right_away': False}


class PartingStep(Step):
    def __init__(self, **kwargs):
        self.set_answer_text('Всего доброго! Я подожду здесь. Всегда буду рад помочь.')
        self.add_client_answer_case(self.run_anyway)

    def run_anyway(self, string):
        return {'next_step': 'OfferToHelpStep', 'right_away': False}


class OfferToChooseDirectionStep(Step):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.set_answer_text('Выберите направление продукта, которое вас интересует:')
        self.set_send_buttons(True)

        self.set_buttons(get_directions(**kwargs))

        self.add_client_answer_case(self.accept)

    def accept(self, string):
        if string == 'да':
            return {'next_step': 'OfferToChooseMoreDirectionsStep', 'right_away': False}


class OfferToChooseMoreDirectionsStep(Step):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.set_answer_text('Хотите выбрать еще одно направление?')
        self.set_send_buttons(True)
        self.set_buttons(['да', 'нет'])

        self.add_client_answer_case(self.selected_in_product_directions)

    def selected_in_product_directions(self, string):
        if string in get_directions(**self.kwargs):
            add_to_selected_categories(**self.kwargs)
            return {'next_step': 'OfferToChooseBranchOfApplicationStep', 'right_away': False}


class OfferToChooseBranchOfApplicationStep(Step):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.set_answer_text('Выберите отрасль применения продукта, которая вас интересует:')
        self.set_send_buttons(True)

        self.set_buttons(get_branches_of_application(**kwargs))

        self.add_client_answer_case(self.accept)
        self.add_client_answer_case(self.decline)

    def accept(self, string):
        if string == 'да':
            return {'next_step': 'OfferToChooseMoreBranchesOfApplicationStep', 'right_away': False}

    def decline(self, string):
        if string == 'нет':
            return {'next_step': 'OfferToChooseBranchOfApplicationStep', 'right_away': False}


class OfferToChooseMoreBranchesOfApplicationStep(Step):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.set_answer_text('Хотите выбрать еще одну отрасль применения?')
        self.set_send_buttons(True)
        self.set_buttons(['да', 'нет'])

        self.add_client_answer_case(self.selected_in_product_branches_of_application)

    def selected_in_product_branches_of_application(self, string):
        if string in get_branches_of_application(**self.kwargs):
            add_to_selected_categories(**self.kwargs)
            return {'next_step': 'OfferToChooseMoreBranchesOfApplicationStep', 'right_away': False}


class SendingProductsStep(Step):
    def __init__(self, **kwargs):
        self.set_answer_text(get_products_from_categories_text(**kwargs))

        self.add_client_answer_case(self.accept)
        self.add_client_answer_case(self.decline)

    def accept(self, string):
        if string == 'да':
            return {'next_step': 'OfferToChooseBranchOfApplicationStep', 'right_away': False}

    def decline(self, string):
        if string == 'нет':
            return {'next_step': 'SendingProductsStep', 'right_away': False}


class OfferToFindRelatedCoursesStep(Step):
    def __init__(self, **kwargs):
        self.set_answer_text('Хотите посмотреть учебные курсы по найденным продуктам?')
        self.set_send_buttons(True)
        self.set_buttons(['да', 'нет'])

        self.add_client_answer_case(self.run_anyway)

    def run_anyway(self, string):
        return {'next_step': 'OfferToFindRelatedCoursesStep', 'right_away': True}


class SendingCoursesStep(Step):
    def __init__(self, **kwargs):
        self.set_answer_text(get_related_courses(**kwargs))

        self.add_client_answer_case(self.accept)
        self.add_client_answer_case(self.decline)

    def accept(self, string):
        if string == 'да':
            return {'next_step': 'SendingCoursesStep', 'right_away': False}

    def decline(self, string):
        if string == 'нет':
            return {'next_step': 'PartingStep', 'right_away': False}
