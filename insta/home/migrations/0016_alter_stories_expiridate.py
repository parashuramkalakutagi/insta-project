# Generated by Django 4.2.4 on 2023-08-13 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_stories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stories',
            name='expiridate',
            field=models.DateTimeField(),
        ),
    ]
