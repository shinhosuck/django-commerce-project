# Generated by Django 3.1.5 on 2021-03-18 14:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0009_auto_20210318_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='user_name',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer_address', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
