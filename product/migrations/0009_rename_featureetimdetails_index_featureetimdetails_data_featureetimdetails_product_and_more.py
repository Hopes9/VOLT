# Generated by Django 4.2.1 on 2023-05-04 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_featureetimdetails_data_featurevalue'),
    ]

    operations = [
        migrations.RenameField(
            model_name='featureetimdetails_data',
            old_name='featureETIMDetails_index',
            new_name='featureETIMDetails_product',
        ),
        migrations.AddField(
            model_name='featureetimdetails_data',
            name='featureETIMDetails',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.featureetimdetails'),
        ),
    ]
