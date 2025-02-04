# Generated by Django 5.0.6 on 2024-05-15 07:25

import app.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('image', models.ImageField(default='products/default.jpg', upload_to=app.models.upload_to, verbose_name='Image')),
                ('description', models.TextField(null=True)),
                ('slug', models.SlugField(max_length=250, unique_for_date='published')),
                ('status', models.CharField(choices=[('outofstock', 'Out of Stock'), ('available', 'Available')], default='available', max_length=10)),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='app.category')),
            ],
        ),
    ]
