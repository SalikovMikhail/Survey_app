# Generated by Django 2.2.10 on 2020-11-14 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0002_user_userresponses_usersurvey'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersurvey',
            name='current_count_responses',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='usersurvey',
            name='total_responses',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
