# Generated by Django 2.2.1 on 2019-05-21 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tweeter', '0006_auto_20190521_1505'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('not_tweet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tweeter.Tweet')),
                ('notified', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tweeter.TweeterUser')),
            ],
        ),
    ]
