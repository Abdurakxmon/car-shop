# Generated by Django 3.1.7 on 2021-03-28 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='hot',
        ),
    ]
