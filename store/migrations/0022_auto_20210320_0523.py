# Generated by Django 3.1.5 on 2021-03-20 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_auto_20210320_0446'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='open_order',
            field=models.BooleanField(default=True),
        ),
    ]