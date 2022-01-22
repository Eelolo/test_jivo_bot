from django.db import models
from django.contrib.postgres.fields import ArrayField


class Chat(models.Model):
    chat_id = models.PositiveIntegerField(verbose_name='Jivo chat id')
    client_id = models.ForeignKey('ChatClient', on_delete=models.CASCADE)
    step = models.CharField(max_length=150, default='')
    selected_categories = ArrayField(
        models.PositiveIntegerField(verbose_name='category id'),
        default=list
    )


class ChatClient(models.Model):
    client_id = models.PositiveIntegerField(verbose_name='Jivo client id')
    name = models.CharField(max_length=150, null=True, blank=True, verbose_name='Имя')
    phone = models.CharField(max_length=25, null=True, blank=True, verbose_name='Телефон')
    email = models.EmailField(null=True, blank=True, verbose_name='Телефон')


class Message(models.Model):
    client_id = models.ForeignKey('ChatClient', on_delete=models.CASCADE)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    text = models.TextField(default='')
    bot = models.BooleanField()  # если True, означает, что это сообщение от бота к пользователю
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
