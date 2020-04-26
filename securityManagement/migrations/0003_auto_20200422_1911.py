# Generated by Django 3.0.4 on 2020-04-22 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('securityManagement', '0002_recipient_register_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipient',
            name='email',
            field=models.EmailField(error_messages={'unique': 'The email is already being used by a recipient.'}, max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='recipient',
            name='register_num',
            field=models.IntegerField(unique=True),
        ),
    ]