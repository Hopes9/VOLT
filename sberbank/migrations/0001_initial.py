# Generated by Django 4.2.1 on 2023-05-04 08:25

from django.db import migrations, models
import django.db.models.deletion
import sberbank.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('payment_id', models.UUIDField(blank=True, db_index=True, null=True, verbose_name='payment ID')),
                ('bank_id', models.UUIDField(blank=True, db_index=True, null=True, verbose_name='bank payment ID')),
                ('action', models.CharField(db_index=True, max_length=100, verbose_name='action')),
                ('request_text', models.TextField(blank=True, null=True, verbose_name='request text')),
                ('response_text', models.TextField(blank=True, null=True, verbose_name='response text')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created')),
                ('checksum', models.CharField(blank=True, db_index=True, max_length=256, null=True)),
            ],
            options={
                'verbose_name': 'log entry',
                'verbose_name_plural': 'log entries',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(db_index=True, editable=False, primary_key=True, serialize=False, unique=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('bank_id', models.UUIDField(blank=True, db_index=True, null=True, verbose_name='bank ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=128, verbose_name='amount')),
                ('error_code', models.PositiveIntegerField(blank=True, null=True, verbose_name='error code')),
                ('error_message', models.TextField(blank=True, null=True, verbose_name='error message')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'CREATED'), (1, 'PENDING'), (2, 'SUCCEEDED'), (3, 'FAILED'), (4, 'REFUNDED')], db_index=True, default=sberbank.models.Status['CREATED'], verbose_name='status')),
                ('details', models.JSONField(blank=True, null=True, verbose_name='details')),
                ('client_id', models.TextField(blank=True, null=True, verbose_name='client ID')),
                ('method', models.PositiveSmallIntegerField(choices=[(0, 'UNKNOWN'), (1, 'WEB'), (2, 'APPLE'), (3, 'GOOGLE')], db_index=True, default=sberbank.models.Method['UNKNOWN'], verbose_name='method')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, verbose_name='modified')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
            ],
            options={
                'verbose_name': 'payment',
                'verbose_name_plural': 'payments',
                'ordering': ['-updated'],
            },
        ),
    ]
