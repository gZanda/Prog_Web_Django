# Generated by Django 4.2.7 on 2023-11-04 01:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_app', '0003_user_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
    ]
