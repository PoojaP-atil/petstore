# Generated by Django 4.2.7 on 2024-01-17 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0012_alter_order_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ordernumber',
            field=models.CharField(default=0, max_length=200),
        ),
    ]