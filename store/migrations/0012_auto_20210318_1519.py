# Generated by Django 3.1.5 on 2021-03-18 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20210318_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.customer'),
        ),
    ]
