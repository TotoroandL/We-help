# Generated by Django 2.1.1 on 2018-12-22 03:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0002_auto_20181220_0923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='collection_buy_times',
        ),
        migrations.RemoveField(
            model_name='user',
            name='collection_delivery_times',
        ),
        migrations.RemoveField(
            model_name='user',
            name='collection_others_times',
        ),
        migrations.RemoveField(
            model_name='user',
            name='collection_print_times',
        ),
        migrations.RemoveField(
            model_name='user',
            name='collection_umbrella_times',
        ),
    ]
