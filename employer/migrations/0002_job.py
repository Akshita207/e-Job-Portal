# Generated by Django 4.2.5 on 2023-09-25 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150)),
                ('logo', models.ImageField(blank=True, upload_to='')),
                ('company_name', models.CharField(max_length=300)),
                ('location', models.CharField(max_length=150)),
                ('about', models.CharField(max_length=3000)),
                ('qualifications', models.CharField(blank=True, max_length=3000)),
                ('responsibility', models.CharField(blank=True, max_length=3000)),
                ('experience', models.IntegerField(blank=True)),
                ('job_type', models.CharField(blank=True, max_length=50)),
                ('package', models.CharField(blank=True, max_length=150)),
                ('skills', models.CharField(blank=True, max_length=350)),
                ('status', models.CharField(default='pending', max_length=50)),
                ('employer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employer.employer')),
            ],
        ),
    ]
