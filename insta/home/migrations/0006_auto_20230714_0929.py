# Generated by Django 3.1.8 on 2023-07-14 03:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20230714_0832'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='likes',
            unique_together=set(),
        ),
    ]
