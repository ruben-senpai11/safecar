# Generated by Django 4.0.4 on 2022-05-16 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('safecar', '0023_notification_errors_alter_operation_is_expired'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operation',
            name='is_expired',
        ),
    ]
