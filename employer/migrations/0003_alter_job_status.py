# Generated by Django 4.2.5 on 2023-09-25 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0002_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(max_length=50),
        ),
    ]