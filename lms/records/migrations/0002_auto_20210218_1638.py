# Generated by Django 3.1.5 on 2021-02-18 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thing',
            name='code',
            field=models.CharField(max_length=10, primary_key=True, serialize=False, unique=True),
        ),
    ]
