# Generated by Django 2.2.1 on 2019-05-12 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweeter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweeteruser',
            name='name',
            field=models.TextField(default='no name provided', max_length=30),
        ),
    ]
