# Generated by Django 3.1.2 on 2020-10-18 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0003_skillanswer_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='skillanswer',
            name='processed_answer',
            field=models.TextField(default='heyy'),
        ),
        migrations.AddField(
            model_name='skillanswer',
            name='sentiment',
            field=models.FloatField(default=0.0),
        ),
    ]
