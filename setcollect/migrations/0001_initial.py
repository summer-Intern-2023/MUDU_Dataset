# Generated by Django 4.2.3 on 2023-07-14 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Sentences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentences', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_degree', models.CharField(max_length=16)),
                ('tag_classification', models.CharField(max_length=16)),
                ('tag_name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('title_tag', models.ManyToManyField(to='setcollect.tag')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=64)),
                ('role', models.SmallIntegerField(choices=[(1, 'admin'), (2, 'user')], verbose_name='choice of role')),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=128)),
                ('sentences', models.ManyToManyField(to='setcollect.sentences')),
                ('title', models.ManyToManyField(to='setcollect.title')),
                ('word_tag', models.ManyToManyField(to='setcollect.tag')),
            ],
        ),
        migrations.AddField(
            model_name='sentences',
            name='sentences_tag',
            field=models.ManyToManyField(to='setcollect.tag'),
        ),
        migrations.AddField(
            model_name='sentences',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setcollect.title'),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setcollect.conversation')),
                ('question_tag', models.ManyToManyField(to='setcollect.tag')),
            ],
        ),
        migrations.CreateModel(
            name='LModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lmodel', models.SmallIntegerField(choices=[(1, 'ChatGPT'), (2, 'ChatGLM'), (3, 'Bard'), (4, 'Human')], verbose_name='choice of model')),
                ('answer', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setcollect.question')),
            ],
        ),
    ]
