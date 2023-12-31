# Generated by Django 4.2.2 on 2023-07-18 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setcollect', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sentences',
            name='title',
        ),
        migrations.RemoveField(
            model_name='word',
            name='sentences',
        ),
        migrations.RemoveField(
            model_name='word',
            name='title',
        ),
        migrations.AddField(
            model_name='sentences',
            name='words',
            field=models.ManyToManyField(to='setcollect.word'),
        ),
        migrations.AddField(
            model_name="title",
            name="mapping",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='title',
            name='sentences',
            field=models.ManyToManyField(to='setcollect.sentences'),
        ),
        migrations.AddField(
            model_name='title',
            name='words',
            field=models.ManyToManyField(to='setcollect.word'),
        ),
    ]
