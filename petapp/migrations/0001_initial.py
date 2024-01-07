# Generated by Django 4.2.7 on 2023-12-17 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(upload_to='media')),
                ('Name', models.CharField(max_length=200)),
                ('Species', models.CharField(max_length=200)),
                ('Breed', models.CharField(max_length=200)),
                ('Age', models.IntegerField()),
                ('Gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=200)),
                ('Description', models.CharField(max_length=500)),
                ('Price', models.FloatField()),
            ],
            options={
                'db_table': 'pet',
            },
        ),
    ]
