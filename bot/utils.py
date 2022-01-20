from django.utils import timezone, dateformat
import json
from .models import Message, ChatClient, Chat


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
    def wrapper(bot, **kwargs):
        func(bot, **kwargs)

        chat, chat_client = get_or_create_instances(bot.chat_id, bot.client_id)
        Message.objects.create(
            client_id=chat_client, chat_id=chat.pk, text=kwargs['message'], bot=True
        )

    return wrapper


def get_or_create_instances(chat_id, client_id):
    chat = Chat.objects.filter(chat_id=chat_id).first()
    chat_client = ChatClient.objects.filter(client_id=client_id).first()

    if not chat_client:
        chat_client = ChatClient.objects.create(client_id=client_id)
    if not chat:
        chat = Chat.objects.create(chat_id=chat_id, client_id=chat_client, status=1)

    return chat, chat_client
