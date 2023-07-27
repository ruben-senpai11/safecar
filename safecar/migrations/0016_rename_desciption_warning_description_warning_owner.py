# Generated by Django 4.0.4 on 2022-05-08 00:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('safecar', '0015_rename_desciption_operation_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='warning',
            old_name='desciption',
            new_name='description',
        ),
        migrations.AddField(
            model_name='warning',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='safecar.owner', verbose_name='Propriétaire'),
        ),
    ]