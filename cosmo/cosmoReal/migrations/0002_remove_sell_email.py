# Generated by Django 2.2.20 on 2021-04-25 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cosmoReal', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sell',
            name='email',
        ),
    ]
