# Generated by Django 2.2.10 on 2020-11-15 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0004_auto_20201115_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='userresponses',
            name='id_survey',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_responses', to='question.Survey'),
        ),
    ]
