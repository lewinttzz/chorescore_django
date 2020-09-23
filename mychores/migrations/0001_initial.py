# Generated by Django 2.2.16 on 2020-09-20 10:40

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('description', models.CharField(help_text="What's the name of the task?", max_length=20, primary_key='true', serialize=False)),
                ('isRecurrent', models.BooleanField(help_text='Should the task be repeated in regular time intervals or on demand?', verbose_name='Recurrent')),
                ('recurrenceFrequency', models.DurationField(blank=True, help_text='How often does the task need to be done?', null=True)),
                ('maxScore', models.IntegerField(help_text='What is the maximum achievable score for task completion?')),
                ('state', models.CharField(choices=[('o', 'inactive'), ('a', 'active')], default='a', max_length=200)),
                ('details', models.CharField(blank=True, help_text='What needs to be done?', max_length=2000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task_Instance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID', primary_key=True, serialize=False)),
                ('state', models.CharField(choices=[('u', 'upcoming'), ('d', 'due'), ('o', 'overdue'), ('p', 'verification pending'), ('e', 'expired'), ('f', 'finished')], default='d', max_length=200)),
                ('dueDate', models.DateField(default=datetime.date.today)),
                ('mostRecentInstance', models.BooleanField(blank=True, default=True, null=True)),
                ('assignedProfile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mychores.Profile')),
                ('taskTbd', models.ForeignKey(blank=True, help_text='What kind of task?', null=True, on_delete=django.db.models.deletion.CASCADE, to='mychores.Task')),
                ('verifiedBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='verificationBy', to='mychores.Profile')),
            ],
        ),
    ]
