# Generated by Django 4.2.5 on 2023-09-23 07:50

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeRole',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('user.user',),
            managers=[
                ('employee', django.db.models.manager.Manager()),
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('photo', models.ImageField(blank=True, default='avatar.png', upload_to='')),
                ('location', models.CharField(blank=True, max_length=200)),
                ('achievement', jsonfield.fields.JSONField()),
                ('phone_no', models.CharField(blank=True, max_length=15)),
                ('primary_role', models.CharField(blank=True, max_length=50)),
                ('experience', models.IntegerField(blank=True, null=True)),
                ('secondary_role', models.CharField(blank=True, max_length=150)),
                ('bio', models.CharField(blank=True, max_length=250)),
                ('resume', models.FileField(blank=True, default=None, upload_to='')),
                ('social_profiles', jsonfield.fields.JSONField()),
                ('work_experience', jsonfield.fields.JSONField()),
                ('education', jsonfield.fields.JSONField()),
                ('skills', models.CharField(blank=True, max_length=350)),
                ('availability', models.CharField(blank=True, max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
