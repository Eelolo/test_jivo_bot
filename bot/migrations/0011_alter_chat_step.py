# Generated by Django 3.2.11 on 2022-01-23 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0010_alter_chat_step'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='step',
            field=models.CharField(default='', max_length=150),
        ),
    ]