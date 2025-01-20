# Generated by Django 5.1.1 on 2025-01-20 17:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_borrow_datereturn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='borrowedBy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrows', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateReserved', models.DateTimeField(auto_now_add=True)),
                ('isActive', models.BooleanField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserve_book', to='api.book')),
                ('reservedBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserved', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('book', 'reservedBy', 'isActive')},
            },
        ),
    ]
