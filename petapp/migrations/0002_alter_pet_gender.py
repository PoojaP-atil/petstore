# Generated by Django 4.2.7 on 2023-12-17 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='Gender',
            field=models.CharField(choices=[('Male', 'male'), ('Female', 'female')], max_length=200),
        ),
    ]