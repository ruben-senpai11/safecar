# Generated by Django 4.0.4 on 2022-05-06 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('safecar', '0014_rename_typeoperation_operation_type_operation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operation',
            old_name='desciption',
            new_name='description',
        ),
    ]