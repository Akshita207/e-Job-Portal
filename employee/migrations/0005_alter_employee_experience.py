# Generated by Django 4.2.5 on 2023-09-25 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_alter_employee_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='experience',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]