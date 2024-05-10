# Generated by Django 5.0.4 on 2024-05-09 22:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAdditional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=40, verbose_name='full_name')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name='phone')),
                ('otp_verify', models.BooleanField(default=False, verbose_name='Phone Number Verify Status')),
                ('opt_expire_date', models.DateTimeField(blank=True, null=True, verbose_name='OTP Expire Date')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
        ),
    ]
