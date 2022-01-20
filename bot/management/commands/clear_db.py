from django.core.management.base import BaseCommand
from bot.models import Chat, ChatClient, Message


class Command(BaseCommand):
    def handle(self, *args, **options):
        [chat.delete() for chat in Chat.objects.all()]
        [chat_client.delete() for chat_client in ChatClient.objects.all()]
        [message.delete() for message in Message.objects.all()]
