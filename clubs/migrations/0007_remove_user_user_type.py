# Generated by Django 3.2.5 on 2021-11-26 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0006_user_user_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_type',
        ),
    ]
