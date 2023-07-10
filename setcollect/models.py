from django.db import models

# Create your models here.

"""
   Conversation contains a series of questions. question contains a series of LModels and Tags.
    LModel contains a model choice (ChatGPT, ChatGLM, Bard) and an answer.
"""


class UserInfo(models.Model):
    role_choice = (
        (1, "admin"),
        (2, "user"),
    )

    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    role = models.SmallIntegerField(verbose_name="choice of role", choices=role_choice)


class Conversation(models.Model):
    name = models.CharField(max_length=64)


class Question(models.Model):
    question = models.TextField()
    conversation = models.ForeignKey("Conversation", on_delete=models.CASCADE)


class LModel(models.Model):
    model_choice = (
        (1, "ChatGPT"),
        (2, "ChatGLM"),
        (3, "Bard"),
    )

    lmodel = models.SmallIntegerField(
        verbose_name="choice of model", choices=model_choice
    )
    answer = models.TextField()

    question = models.ForeignKey("Question", on_delete=models.CASCADE)


class Tag(models.Model):
    tag_name = models.CharField(max_length=32)
    question = models.ManyToManyField("Question")
