# Generated by Django 5.1.1 on 2025-02-17 13:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_borrow_borrowedby_reserve'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=255)),
                ('transactionDate', models.DateField()),
                ('bookId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book', to='api.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
