# Generated by Django 2.2.28 on 2024-11-17 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airport', '0007_character_end_time_countdown'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='crashed',
            field=models.BooleanField(null=True),
        ),
    ]
