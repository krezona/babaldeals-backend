# Generated by Django 5.0.6 on 2024-06-06 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.CharField(),
        ),
    ]
