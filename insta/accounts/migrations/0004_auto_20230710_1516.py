# Generated by Django 3.1.8 on 2023-07-10 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='otp',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
