# Generated by Django 4.2.2 on 2023-06-08 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_remove_product_mrc_product_lastupddate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='LastUpdDate',
            field=models.DateField(blank=True, null=True, verbose_name='Последнее обновление'),
        ),
    ]
