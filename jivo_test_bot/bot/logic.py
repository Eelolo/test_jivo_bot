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
        'offer_to_choose_branch_of_application': 'Выберите область применения продукта, которая вас интересуют:',
        'offer_to_choose_more_branches_of_application': 'Хотите выбрать еще одну область применения?',
        'sending_products': 'Продукты подходящие к выбранным категориям:\n'
    }

    CLIENT_RESPONSES = {
        'accept': 'Да, пожалуйста.',
        'decline': 'Нет, спасибо.',
        'help_not_needed': 'Спасибо, я справлюсь.'
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
        if self.event == 'CLIENT_MESSAGE':
            if self.chat_status == 10 and self.message == self.CLIENT_RESPONSES['help_not_needed']:
                self.update_chat_status(0)
                self.parting()
            elif self.chat_status == 10 and self.message == self.CLIENT_RESPONSES['accept']:
                self.update_chat_status(11)
                self.offer_to_choose_direction()
            elif self.chat_status == 10 and self.message == self.CLIENT_RESPONSES['decline'] or \
                    self.chat_status == 12 and self.message == self.CLIENT_RESPONSES['accept']:
                self.update_chat_status(13)
                self.offer_to_choose_branch_of_application()
            elif self.chat_status == 12 and self.message == self.CLIENT_RESPONSES['decline']:
                self.update_chat_status(0)
                self.send_products()
            elif self.chat_status == 11:
                self.update_chat_status(10)
                self.offer_to_choose_more_directions()
            elif self.chat_status == 13:
                self.update_chat_status(12)
                self.offer_to_choose_more_branches_of_application()
            elif self.chat_status == 0:
                self.update_chat_status(1)
                self.greetings()
                self.offer_to_help()
                self.update_chat_status(10)

            categories = self.get_categories()  # здесь очень неэффективно!!
            if self.message in list(self.directions.values()) + list(self.branches_of_application.values()):
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

    def greetings(self):
        self.send_text_message(message=self.RESPONSES['greetings'])

    def offer_to_help(self):
        buttons = (self.CLIENT_RESPONSES['accept'], self.CLIENT_RESPONSES['decline'])
        self.send_buttons_message(message=self.RESPONSES['offer_to_help'], buttons=buttons)

    def offer_to_choose_direction(self):
        categories = self.get_categories()[0]
        self.send_buttons_message(message=self.RESPONSES['offer_to_choose_direction'], buttons=categories)

    def offer_to_choose_more_directions(self):
        buttons = (self.CLIENT_RESPONSES['accept'], self.CLIENT_RESPONSES['decline'])
        self.send_buttons_message(
            message=self.RESPONSES['offer_to_choose_more_directions'],
            buttons=buttons
        )

    def offer_to_choose_branch_of_application(self):
        categories = self.get_categories()[1]
        self.send_buttons_message(message=self.RESPONSES['offer_to_choose_branch_of_application'], buttons=categories)

    def offer_to_choose_more_branches_of_application(self):
        buttons = (self.CLIENT_RESPONSES['accept'], self.CLIENT_RESPONSES['decline'])
        self.send_buttons_message(
            message=self.RESPONSES['offer_to_choose_more_branches_of_application'],
            buttons=buttons
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
