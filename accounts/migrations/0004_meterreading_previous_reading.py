# Generated by Django 5.0.6 on 2024-07-19 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_meterreading_previous_reading_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='meterreading',
            name='previous_reading',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
