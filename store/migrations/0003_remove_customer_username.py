# Generated by Django 3.1.5 on 2021-03-16 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20210316_0749'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='username',
        ),
    ]