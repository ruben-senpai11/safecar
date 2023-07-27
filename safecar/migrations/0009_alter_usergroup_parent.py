# Generated by Django 4.0.4 on 2022-04-26 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('safecar', '0008_usergroup_user_usergroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergroup',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='safecar.usergroup', verbose_name='Groupe parent'),
        ),
    ]