# Generated by Django 2.2.16 on 2020-09-20 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mychores', '0011_auto_20200920_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='isActive',
            field=models.BooleanField(default=False),
        ),
    ]
