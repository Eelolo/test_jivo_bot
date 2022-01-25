from bot.cadfem_jivo_bot.steps import Step
from bot.utils import (
    get_directions, get_branches_of_application, add_to_selected_categories,
    get_products_from_categories_text, get_related_courses, save_client_name,
    save_client_phone
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
            return {'next_step': 'OfferToSpecifyContactsStep', 'right_away': False}

    def decline(self, string):
        if string == 'нет':
            return {'next_step': 'PartingStep', 'right_away': False}


class PartingStep(Step):
    def __init__(self, **kwargs):
        self.set_answer_text('Всего доброго! Я подожду здесь. Всегда буду рад помочь.')
        self.add_client_answer_case(self.run_anyway)

    def run_anyway(self, string):
        return {'next_step': 'OfferToHelpStep', 'right_away': False}


class OfferToSpecifyContactsStep(Step):
    def __init__(self, **kwargs):
        self.set_answer_text('Оставьте нам свои контакты и, при необходимости, мы обязательно вам поможем.')
        self.set_send_buttons(True)
        self.set_buttons(['да', 'нет'])

        self.add_client_answer_case(self.accept)
        self.add_client_answer_case(self.decline)

    def accept(self, string):
        if string == 'да':
            return {'next_step': 'SpecifyNameStep', 'right_away': False}

    def decline(self, string):
        if string == 'нет':
            return {'next_step': 'OfferToChooseDirectionStep', 'right_away': False}


class SpecifyNameStep(Step):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.set_answer_text('Напишите как к вам можно будет обратиться.')
        self.add_client_answer_case(self.run_anyway)

    def run_anyway(self, string):
        save_client_name(**self.kwargs)
        return {'next_step': 'SpecifyPhoneStep', 'right_away': False}


class SpecifyPhoneStep(Step):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.set_answer_text('Укажите ваш номер телефона.')
        self.add_client_answer_case(self.run_anyway)

    def run_anyway(self, string):
        save_client_phone(**self.kwargs)
        return {'next_step': 'AcceptSpecifyingContactsStep', 'right_away': True}


class AcceptSpecifyingContactsStep(Step):
    def __init__(self, **kwargs):
        self.set_answer_text('Спасибо, теперь мы точно сможем вам помочь, в случае возникновения проблем.')
        self.add_client_answer_case(self.run_anyway)

    def run_anyway(self, string):
        return {'next_step': 'OfferToChooseDirectionStep', 'right_away': True}


class OfferToChooseDirectionStep(Step):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.set_answer_text('Выберите направление продукта, которое вас интересует:')
        self.set_send_buttons(True)

        self.directions = get_directions(**kwargs)
        self.set_buttons(self.directions + ['Выбрать другое направление'])

        self.add_client_answer_case(self.selected_in_product_directions)
        self.add_client_answer_case(self.select_other_category)

    def selected_in_product_directions(self, string):
        if string in self.directions:
            add_to_selected_categories(**self.kwargs)
            return {'next_step': 'OfferToChooseBranchOfApplicationStep', 'right_away': False}

    def select_other_category(self, string):
        if string == 'Выбрать другое направление':
            return {'next_step': 'ChooseOtherDirectionsStep', 'right_away': False}


class ChooseOtherDirectionsStep(Step):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.set_answer_text('Выберите направление продукта, которое вас интересует:')
        self.set_send_buttons(True)

        self.directions = get_directions(**kwargs)
        self.set_buttons(self.directions + ['Вернуться к основным направлениям'])

        self.add_client_answer_case(self.selected_in_product_directions)
        self.add_client_answer_case(self.select_featured_category)

    def selected_in_product_directions(self, string):
        if string in self.directions:
            add_to_selected_categories(**self.kwargs)
            return {'next_step': 'OfferToChooseBranchOfApplicationStep', 'right_away': False}

    def select_featured_category(self, string):
        if string == 'Вернуться к основным направлениям':
            return {'next_step': 'OfferToChooseDirectionStep', 'right_away': False}


class OfferToChooseBranchOfApplicationStep(Step):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.set_answer_text('Выберите отрасль применения продукта, которая вас интересует:')
        self.set_send_buttons(True)

        self.get_branches_of_application = get_branches_of_application(**kwargs)
        self.set_buttons(self.get_branches_of_application + ['Выбрать другую отрасль применения'])

        self.add_client_answer_case(self.selected_in_product_branches_of_application)
        self.add_client_answer_case(self.select_other_category)

    def selected_in_product_branches_of_application(self, string):
        if string in self.get_branches_of_application:
            add_to_selected_categories(**self.kwargs)
            return {'next_step': 'SendingProductsStep', 'right_away': False}

    def select_other_category(self, string):
        if string == 'Выбрать другую отрасль применения':
            return {'next_step': 'ChooseOtherBranchOfApplicationStep', 'right_away': False}


class ChooseOtherBranchOfApplicationStep(Step):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.set_answer_text('Выберите отрасль применения продукта, которая вас интересует:')
        self.set_send_buttons(True)

        self.get_branches_of_application = get_branches_of_application(**kwargs)
        self.set_buttons(self.get_branches_of_application + ['Вернуться к основным областям применения'])

        self.add_client_answer_case(self.selected_in_product_branches_of_application)
        self.add_client_answer_case(self.select_featured_category)

    def selected_in_product_branches_of_application(self, string):
        if string in self.get_branches_of_application:
            add_to_selected_categories(**self.kwargs)
            return {'next_step': 'SendingProductsStep', 'right_away': False}

    def select_featured_category(self, string):
        if string == 'Вернуться к основным областям применения':
            return {'next_step': 'OfferToChooseBranchOfApplicationStep', 'right_away': False}


class SendingProductsStep(Step):
    def __init__(self, **kwargs):
        self.set_answer_text(get_products_from_categories_text(**kwargs))
        self.add_client_answer_case(self.run_anyway)

    def run_anyway(self, string):
        return {'next_step': 'OfferToFindRelatedCoursesStep', 'right_away': False}


class OfferToFindRelatedCoursesStep(Step):
    def __init__(self, **kwargs):
        self.set_answer_text('Хотите посмотреть учебные курсы по найденным продуктам?')
        self.set_send_buttons(True)
        self.set_buttons(['да', 'нет'])

        self.add_client_answer_case(self.accept)
        self.add_client_answer_case(self.decline)

    def accept(self, string):
        if string == 'да':
            return {'next_step': 'SendingCoursesStep', 'right_away': True}

    def decline(self, string):
        if string == 'нет':
            return {'next_step': 'PartingStep', 'right_away': False}


class SendingCoursesStep(Step):
    def __init__(self, **kwargs):
        self.set_answer_text(get_related_courses(**kwargs))
        self.add_client_answer_case(self.run_anyway)

    def run_anyway(self, string):
        return {'next_step': 'PartingStep', 'right_away': False}
