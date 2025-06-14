# Generated by Django 5.1.1 on 2025-05-22 11:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_fine'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=100)),
                ('reference', models.CharField(max_length=200, unique=True)),
                ('transactionDate', models.DateField()),
                ('status', models.CharField(default='pending', max_length=50)),
                ('bookId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookid', to='api.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
