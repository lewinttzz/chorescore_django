# Generated by Django 2.2.16 on 2020-09-20 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mychores', '0002_auto_20200920_1244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task_instance',
            name='jeffDate',
        ),
    ]