# Generated by Django 5.0.6 on 2024-05-16 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_product_stock_alter_product_price_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=250, unique=True),
        ),
    ]
