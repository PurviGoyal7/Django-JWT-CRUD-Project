# Generated by Django 4.2.4 on 2023-08-14 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_rename_email_data_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='data',
            old_name='user_id',
            new_name='user',
        ),
    ]