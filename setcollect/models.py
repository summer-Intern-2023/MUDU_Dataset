from django.db import models


class UserInfo(models.Model):
    role_choice = (
        (1, "admin"),
        (2, "user"),
    )

    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    role = models.SmallIntegerField(verbose_name="choice of role", choices=role_choice)


class Conversation(models.Model):
    name = models.TextField()


class Question(models.Model):
    question = models.TextField()
    conversation = models.ForeignKey("Conversation", on_delete=models.CASCADE)
    question_tag = models.ManyToManyField("Tag")


class LModel(models.Model):
    model_choice = (
        (1, "ChatGPT"),
        (2, "iflytek spark"),
        (3, "Human"),
        (4, "Mudu V1.0"),
        (5, "Mudu V2.0"),
        (6, "Mudu V3.0"),
        (7, "Mudu V4.0"),
        (8, "Mudu V5.0"),
        (9, "Mudu V6.0"),
    )

    lmodel = models.SmallIntegerField(
        verbose_name="choice of model", choices=model_choice
    )
    answer = models.TextField()
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    evaluation = models.IntegerField()


class Tag(models.Model):
    tag_degree = models.CharField(max_length=16 , null=True) 
    tag_classification = models.CharField(max_length=16)
    tag_name = models.CharField(max_length=32)


class Word(models.Model):
    word = models.CharField(max_length=128)
    word_tag = models.ManyToManyField("Tag")


class Sentences(models.Model):
    sentences = models.TextField()
    words = models.ManyToManyField("Word")
    sentences_tag = models.ManyToManyField("Tag")


class Title(models.Model):
    title = models.TextField()
    words = models.ManyToManyField("Word")
    sentences = models.ManyToManyField("Sentences")
    title_tag = models.ManyToManyField("Tag")
    mapping = models.BooleanField(default=False)
