# Generated by Django 3.2.5 on 2021-11-26 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0006_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(default='APPLICANT', max_length=20),
        ),
    ]
