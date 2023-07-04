# Generated by Django 4.2.2 on 2023-07-04 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("setcollect", "0003_rename_question_from_lmodel_question"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="question",
            name="tag_name",
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tag_name", models.CharField(max_length=32)),
                ("question", models.ManyToManyField(to="setcollect.question")),
            ],
        ),
    ]
