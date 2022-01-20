from django.db import models
from django.contrib.postgres.fields import ArrayField


class Chat(models.Model):
    chat_id = models.PositiveIntegerField(verbose_name='Jivo chat id')
    client_id = models.ForeignKey('ChatClient', on_delete=models.CASCADE)
    status = models.PositiveIntegerField(default=0)
    selected_categories = ArrayField(
        models.PositiveIntegerField(verbose_name='category id'),
        default=list
    )

    """
        status указывает на состояние сценария. При добавлении в логику новых пропиши сюда что и зачем
        0 - сценарий окончен
        1 - сценарий начат
        10 - предложено выбрать категорию направление продукта 1010 - активировать принудительно
        11 - предложено выбрать еще одно направление продукта 1111 - активировать принудительно
        20 - предложено выбрать категорию отрасль применения 2020 - активировать принудительно
        21 - предложено выбрать еще одну отрасль применения 2121 - активировать принудительно
        30 - предложение пдобрать учебные курсы по найденным продуктам 3030 - активировать принудительно
    """


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
