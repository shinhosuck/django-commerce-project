# Generated by Django 3.1.5 on 2021-03-13 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onLineStore', '0006_auto_20210313_0416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='purchase',
            field=models.ManyToManyField(related_name='purchase', to='onLineStore.Purchase'),
        ),
    ]