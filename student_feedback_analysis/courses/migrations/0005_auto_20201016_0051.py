# Generated by Django 3.1.2 on 2020-10-15 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20201015_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackform',
            name='feedback_type',
            field=models.CharField(choices=[('prof', 'Professor Feedback'), ('course', 'Course Feedback'), ('other', 'Other')], max_length=100),
        ),
        migrations.AlterField(
            model_name='feedbackform',
            name='sem_type',
            field=models.CharField(choices=[('midsem', 'Mid Semester'), ('endsem', 'End Semester'), ('other', 'Other')], max_length=100),
        ),
    ]
