# Generated by Django 4.0.4 on 2023-01-19 11:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_chat_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 19, 16, 39, 26, 713514)),
        ),
    ]
