# Generated by Django 4.2.5 on 2023-09-25 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0003_alter_job_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='job_type',
            field=models.CharField(blank=True, choices=[('Full Time', 'Full Time'), ('Contract', 'Contract'), ('Internship', 'Internship')], max_length=50),
        ),
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(default='pending', max_length=50),
        ),
    ]
