# Generated by Django 4.0.4 on 2022-05-13 13:19

import computed_property.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('safecar', '0022_operation_is_expired'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='errors',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='operation',
            name='is_expired',
            field=computed_property.fields.ComputedBooleanField(compute_from='_is_expired', default=False, editable=False),
        ),
    ]
