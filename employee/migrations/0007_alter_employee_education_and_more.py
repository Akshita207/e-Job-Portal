# Generated by Django 4.2.5 on 2023-09-25 07:51

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0006_alter_employee_education_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='education',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='work_experience',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
    ]
