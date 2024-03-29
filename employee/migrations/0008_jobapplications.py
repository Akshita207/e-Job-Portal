# Generated by Django 4.2.5 on 2023-09-26 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0005_alter_job_experience'),
        ('employee', '0007_alter_employee_education_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobApplications',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default='pending', max_length=50)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employee')),
                ('job_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employer.job')),
            ],
        ),
    ]
