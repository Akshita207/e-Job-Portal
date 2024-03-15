# Generated by Django 4.2.5 on 2023-09-11 10:06

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployerRole',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('user.user',),
            managers=[
                ('employer', django.db.models.manager.Manager()),
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('photo', models.ImageField(blank=True, default='avatar.png', upload_to='')),
                ('company_address', models.CharField(blank=True, max_length=300)),
                ('company_name', models.CharField(default='abc', max_length=300)),
                ('phone_no', models.CharField(default='12345', max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]