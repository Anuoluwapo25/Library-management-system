# Generated by Django 5.1.1 on 2025-01-03 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='username',
        ),
    ]