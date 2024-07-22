# Generated by Django 5.0.6 on 2024-06-13 09:54

import user.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_alter_myuser_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='profile',
            field=models.ImageField(default='profile_picture/default.jpg', upload_to=user.models.upload_to, verbose_name='Image'),
        ),
    ]
