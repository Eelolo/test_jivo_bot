from django.utils import timezone, dateformat
import json
from .models import Message, ChatClient, Chat
import requests


def get_timestamp():
    return dateformat.format(timezone.now(), 'U')


def deserialize_data(string):
    data = json.loads(string)

    return data


def client_chat_logging(func):
    def wrapper(request):
        data = deserialize_data(request.body)
        chat, chat_client = get_or_create_instances(data['chat_id'], data['client_id'])
        message = data.get('message').get('text') if data.get('message') else ''
        Message.objects.create(
            client_id=chat_client, chat_id=chat.pk, text=message, bot=False
        )

        return func(request)

    return wrapper


def bot_chat_logging(func):
    def wrapper(bot):
        func(bot)

        chat, chat_client = get_or_create_instances(bot.chat_id, bot.client_id)
        Message.objects.create(
            client_id=chat_client, chat_id=chat.pk, text=bot.message_text, bot=True
        )

    return wrapper


def get_or_create_instances(chat_id, client_id):
    chat = Chat.objects.filter(chat_id=chat_id).first()
    chat_client = ChatClient.objects.filter(client_id=client_id).first()

    if not chat_client:
        chat_client = ChatClient.objects.create(client_id=client_id)
    if not chat:
        chat = Chat.objects.create(chat_id=chat_id, client_id=chat_client)

    return chat, chat_client


def get_directions(**kwargs):
    url = 'https://static.my.cadfem-cis.ru/api/shop/containers/categories/'

    if kwargs.get('featured') and kwargs.get('featured') == 'True':
        url += '?featured=True'
    elif kwargs.get('featured') and kwargs.get('featured') == 'False':
        url += '?featured=False'

    data = deserialize_data(requests.get(url).content)

    directions = []
    for category in data['results'][1]['children']:
        directions.append(category["title"])

    return directions


def get_branches_of_application(**kwargs):
    url = 'https://static.my.cadfem-cis.ru/api/shop/containers/categories/'

    if 'featured' in kwargs.keys() and not kwargs['featured']:
        url += '?featured=False'
    else:
        url += '?featured=True'

    data = deserialize_data(requests.get(url).content)

    branches_of_application = []
    for category in data['results'][2]['children']:
        branches_of_application.append(category["title"])

    return branches_of_application


def add_to_selected_categories(**kwargs):
    chat = Chat.objects.get(chat_id=kwargs['chat_id'])
    chat.selected_categories.append(get_category_id_from_title(kwargs['message_text']))
    chat.save()


def get_selected_categories(chat_id):
    chat = Chat.objects.get(chat_id=chat_id)
    return chat.selected_categories


def get_products_from_categories(categories):
    url = 'https://static.my.cadfem-cis.ru/api/shop/containers/' \
          '?limit=5&fields[]=id&fields[]=short_title&category__in[]=1'  # ?????????????? ???? ?????????????????? ?????????????????????? ????????????????

    for category in categories:
        url += f'&category__in[]={category}'

    data = deserialize_data(requests.get(url).content)['results']
    return data


def get_products_from_categories_text(**kwargs):
    categories = get_selected_categories(kwargs['chat_id'])
    products_data = get_products_from_categories(categories)
    if products_data:
        products = '???????????????? ???????????????????? ?? ?????????????????? ????????????????????:\n'
        for product in products_data:
            products += product['short_title'] + '\n'

        return products
    else:
        return '???? ?????????????????? ???????????????????? ?????????????????? ???? ??????????????.'


def get_category_id_from_title(title):
    url = 'https://static.my.cadfem-cis.ru/api/shop/containers/categories/'
    data = deserialize_data(requests.get(url).content)

    # data['results'][0]['children'] - ???????? ???????????????? (?????????????? ????????, ?????????????????????? ??????????????)

    categories = {}
    for category in data['results'][1]['children']:
        categories[category['title']] = category['id']

    for category in data['results'][2]['children']:
        categories[category['title']] = category['id']

    return categories[title]


def get_related_courses(**kwargs):
    products = get_products_from_categories(get_selected_categories(kwargs['chat_id']))
    from random import randint
    courses = []
    if products:
        for idx in range(randint(0, len(products)), randint(0, len(products)), randint(1, len(products))):
            url = f'https://static.my.cadfem-cis.ru/api/shop/containers/{idx}/learning-course/' \
                  '?limit=5&fields[]=id&fields[]=short_title&f'
            data = deserialize_data(requests.get(url).content).get('results', [])
            titles = [result['short_title'] for result in data]
            courses.extend(titles)

        courses = '\n\n'.join(courses)

    if not products or not courses:
        return '???? ?????????????????? ???????????????????? ?????????????? ???????????? ???? ??????????????.'
    else:
        return courses


def save_client_name(**kwargs):
    client = ChatClient.objects.get(client_id=kwargs['client_id'])
    client.name = kwargs['message_text']
    client.save()


def save_client_phone(**kwargs):
    client = ChatClient.objects.get(client_id=kwargs['client_id'])
    client.phone = kwargs['message_text']
    client.save()
