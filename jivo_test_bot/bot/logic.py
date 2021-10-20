from .models import Chat
from .utils import deserialize_data, get_timestamp, bot_chat_logging
import requests


class Bot:
    RESPONSES = {
        'greetings': 'Здраствуйте!',
        'offer_to_help': 'Позвольте помочь вам определиться с выбором продукта.',
        'parting': 'Всего доброго! Я подожду здесь. Всегда буду рад помочь.',
        'offer_to_choose_direction': 'Выберите направление продукта, которое вас интересуют:',
        'offer_to_choose_more_directions': 'Хотите выбрать еще одно направление?',
        'offer_to_choose_branch_of_application': 'Выберите отрасль применения продукта, которая вас интересуют:',
        'offer_to_choose_more_branches_of_application': 'Хотите выбрать еще одну отрасль применения?',
        'sending_products': 'Продукты подходящие к выбранным категориям:\n',
        'offer_to_find_related_courses': 'Хотите посмотреть учебные курсы по найденным продуктам?',
        'sending_courses': 'Курсы по найденным продуктам:\n',
    }

    CLIENT_RESPONSES = {
        'accept': 'Да, пожалуйста.',
        'decline': 'Нет, спасибо.',
        'help_not_needed': 'Спасибо, я справлюсь.'
    }

    CLARIFICATIONS = {
        1: 'В данный момент от вас ожидается подтверждение в формате:\n '
           f'{CLIENT_RESPONSES["accept"]}\n или\n {CLIENT_RESPONSES["help_not_needed"]}',
        10: 'В данный момент от вас ожидается направление продукта.',
        11: f'В данный момент от вас ожидается подтверждение о выборе еще одного направления продукта в формате:\n '
            f'{CLIENT_RESPONSES["accept"]}\n или\n {CLIENT_RESPONSES["decline"]}',
        20: 'В данный момент от вас ожидается отрасль применения продукта.',
        21: f'В данный момент от вас ожидается подтверждение о выборе еще одной отрасли применения в формате:\n '
            f'{CLIENT_RESPONSES["accept"]}\n или\n {CLIENT_RESPONSES["decline"]}',
        'common': 'Чтобы повторить предыдущее действие бота, напишите "еще раз".\n'
                  'Чтобы начать сначала, вы можете написать "рестарт".\n'
                  'Чтобы закончить напишите "пока".',
        31: 'В данный момент от вас ожидается подтверждение в формате:\n '
           f'{CLIENT_RESPONSES["accept"]}\n или\n {CLIENT_RESPONSES["decline"]}',
    }

    COMMANDS = {
        'again': 'еще раз',
        'restart': 'рестарт',
        'stop': 'пока'
    }

    AGAIN_STATUSES = {
        1: 0,
        10: 1010,
        11: 1111,
        20: 2020,
        21: 2121,
        31: 3030,
    }

    def __init__(self, data):
        self.data = data
        self.event_id = data['id']
        self.client_id = data['client_id']
        self.chat_id = data['chat_id']
        self.event = data['event']
        self.message = data.get('message').get('text') if data.get('message') else ''
        self.chat_status = self.get_chat_status()
        self.directions = {}
        self.branches_of_application = {}
        self.get_categories()

        self.classify_event()

    def update_chat_status(self, value):
        chat = Chat.objects.get(chat_id=self.chat_id)
        chat.status = value
        chat.save()
        self.chat_status = chat.status

    def get_chat_status(self):
        chat = Chat.objects.get(chat_id=self.chat_id)
        return chat.status

    def get_selected_categories(self):
        chat = Chat.objects.get(chat_id=self.chat_id)
        return chat.selected_categories

    def add_to_selected_categories(self, category):
        chat = Chat.objects.get(chat_id=self.chat_id)
        chat.selected_categories.append(category)
        chat.save()

    def classify_event(self):
        # print(self.chat_status)
        # print(self.message)

        if self.event == 'CLIENT_MESSAGE':
            if self.chat_status == 0 or self.message == self.COMMANDS['restart']:
                self.update_chat_status(1)
                self.greetings()
                self.offer_to_help()
            # if self.message == 'q':
            #     self.get_related_courses()
            elif self.chat_status == 1 and self.message == self.CLIENT_RESPONSES['help_not_needed'] \
                    or self.message == self.COMMANDS['stop'] \
                    or self.chat_status == 31 and self.message == self.CLIENT_RESPONSES['decline']:
                self.update_chat_status(0)
                self.parting()
            elif self.chat_status in (1, 11) and self.message == self.CLIENT_RESPONSES['accept'] \
                    or self.chat_status == 1010:
                self.update_chat_status(10)
                self.offer_to_choose_direction()
            elif self.chat_status == 10 and self.check_message_in_categories() or self.chat_status == 1111:
                self.update_chat_status(11)
                self.offer_to_choose_more_directions()
            elif self.chat_status == 11 and self.message == self.CLIENT_RESPONSES['decline'] \
                    or self.chat_status == 21 and self.message == self.CLIENT_RESPONSES['accept'] \
                    or self.chat_status == 2020:
                self.update_chat_status(20)
                self.offer_to_choose_branch_of_application()
            elif self.chat_status == 20 and self.check_message_in_categories() or self.chat_status == 2121:
                self.update_chat_status(21)
                self.offer_to_choose_more_branches_of_application()
            elif self.chat_status == 21 and self.message == self.CLIENT_RESPONSES['decline']:
                self.update_chat_status(30)
                self.send_products()
                self.classify_event()
            elif self.chat_status == 30 or self.chat_status == 3030:
                self.update_chat_status(31)
                self.offer_to_find_related_courses()
            elif self.chat_status == 31 and self.message == self.CLIENT_RESPONSES['accept']:
                self.send_related_courses()
                self.update_chat_status(0)
            else:
                if self.message == self.COMMANDS['again']:
                    print('self.message == "еще раз":')
                    self.chat_status = self.AGAIN_STATUSES[self.chat_status]
                    self.classify_event()
                else:
                    self.send_clarifications()

            categories = self.get_categories()  # здесь очень неэффективно!!
            if self.check_message_in_categories():
                common_dict = {}
                common_dict.update(self.directions)
                common_dict.update(self.branches_of_application)
                category = list(common_dict.keys())[list(common_dict.values()).index(self.message)]
                self.add_to_selected_categories(category)

            # self.update_chat_status(0)
        elif self.event == 'INVITE_AGENT':
            pass
        elif self.event == 'AGENT_JOINED':
            pass
        elif self.event == 'AGENT_UNAVAILABLE':
            self.update_chat_status(1)
            self.greetings()
            self.offer_to_help()
            self.update_chat_status(10)
        else:  # CHAT_CLOSED
            pass

    def send_clarifications(self):
        self.send_text_message(message=self.CLARIFICATIONS[self.chat_status])
        self.send_text_message(message=self.CLARIFICATIONS['common'])

    def check_message_in_categories(self):
        return self.message in list(self.directions.values()) + list(self.branches_of_application.values())

    def greetings(self):
        self.send_text_message(message=self.RESPONSES['greetings'])

    def offer_to_help(self):
        buttons = (self.CLIENT_RESPONSES['accept'], self.CLIENT_RESPONSES['help_not_needed'])
        self.send_buttons_message(message=self.RESPONSES['offer_to_help'], buttons=buttons)

    def offer_to_choose_direction(self):
        categories = self.get_categories()[0]
        self.send_buttons_message(message=self.RESPONSES['offer_to_choose_direction'], buttons=categories)

    def offer_to_choose_more_directions(self):
        self.send_buttons_message(
            message=self.RESPONSES['offer_to_choose_more_directions'],
            default_buttons=True
        )

    def offer_to_choose_branch_of_application(self):
        categories = self.get_categories()[1]
        self.send_buttons_message(message=self.RESPONSES['offer_to_choose_branch_of_application'], buttons=categories)

    def offer_to_choose_more_branches_of_application(self):
        self.send_buttons_message(
            message=self.RESPONSES['offer_to_choose_more_branches_of_application'],
            default_buttons=True
        )

    def offer_to_find_related_courses(self):
        self.send_buttons_message(
            message=self.RESPONSES['offer_to_find_related_courses'],
            default_buttons=True
        )

    def parting(self):
        self.send_text_message(message=self.RESPONSES['parting'])

    def send_products(self):
        categories = self.get_selected_categories()
        products_data = self.get_products_from_categories(categories)

        products = ''
        for product in products_data:
            products += product['short_title'] + '\n'

        self.send_text_message(message=self.RESPONSES['sending_products'] + products)

    def send_related_courses(self):
        courses = self.get_related_courses()
        self.send_text_message(message=self.RESPONSES['sending_courses'] + courses)

    @bot_chat_logging
    def send_text_message(self, **kwargs):
        payload = {
            'event': "BOT_MESSAGE",
            'id': self.event_id,
            'client_id': self.client_id,
            'message': {
                'type': "TEXT",
                'text': kwargs['message'],
                'timestamp': get_timestamp(),
            },
        }

        requests.post(
            'https://bot.jivosite.com/webhooks/dFYp2pkeg9lMsRQ/n1G0JfmBvjnXyjA',
            json=payload
        )

    @bot_chat_logging
    def send_buttons_message(self, **kwargs):
        if kwargs.get('default_buttons'):
            kwargs['buttons'] = (self.CLIENT_RESPONSES['accept'], self.CLIENT_RESPONSES['decline'])

        payload = {
            'event': "BOT_MESSAGE",
            'id': self.event_id,
            'client_id': self.client_id,
            'message': {
                'type': "BUTTONS",
                'title': kwargs['message'],
                'buttons': [],
                'timestamp': get_timestamp(),
            },
        }

        for button in kwargs['buttons']:
            payload['message']['buttons'].append({'text': button})

        requests.post(
            'https://bot.jivosite.com/webhooks/dFYp2pkeg9lMsRQ/n1G0JfmBvjnXyjA',
            json=payload
        )

    def get_categories(self):
        url = 'https://static.my.cadfem-cis.ru/api/shop/containers/categories/'
        data = deserialize_data(requests.get(url).content)

        # data['results'][0]['children'] - типы продукта (учебный курс, программный продукт)

        directions = []
        self.directions = {}
        for category in data['results'][1]['children']:
            directions.append(category["title"])
            self.directions[category['id']] = category['title']

        branches_of_application = []
        self.branches_of_application = {}
        for category in data['results'][2]['children']:
            branches_of_application.append(category["title"])
            self.branches_of_application[category['id']] = category['title']

        return directions, branches_of_application

    def get_products_from_categories(self, categories):
        url = 'https://static.my.cadfem-cis.ru/api/shop/containers/' \
              '?fields[]=id&fields[]=short_title&category__in[]=1'  # заранее из категории программные продукты

        for category in categories:
            url += f'&category__in[]={category}'

        data = deserialize_data(requests.get(url).content)['results']

        return data

    def get_related_courses(self):
        products = self.get_products_from_categories(self.get_selected_categories())
        from random import randint

        courses = []
        for idx in range(randint(0, len(products)), randint(0, len(products)), randint(0, len(products))):
            url = f'https://static.my.cadfem-cis.ru/api/shop/containers/{idx}/learning-course/' \
                  '?limit=3&fields[]=id&fields[]=short_title&f'
            data = deserialize_data(requests.get(url).content)['results']
            titles = [result['short_title'] for result in data]
            courses.extend(titles)

        return '\n\n'.join(courses)
