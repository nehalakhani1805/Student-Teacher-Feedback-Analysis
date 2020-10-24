# Generated by Django 3.1.2 on 2020-10-19 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_draftform'),
    ]

    operations = [
        migrations.CreateModel(
            name='DraftQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=225)),
                ('draft_form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.draftform')),
            ],
        ),
    ]