from django.db import models

# Create your models here.

class UserInfo(models.Model):
    role_choice = (
        (1, "admin"),
        (2, "user"),
    )
    
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    role = models.SmallIntegerField(verbose_name="choice of role", choices = role_choice)
    
class Question(models.Model):
    question = models.TextField()
    tag_name = models.CharField(max_length=32)
    

class LModel(models.Model):
    model_choice = (
        (1, "chatGPT"),
        (2, "chatGLM"),
        (3, "bard"),
    )
    
    lmodel = models.SmallIntegerField(verbose_name = "choice of model", choices = model_choice)
    answer = models.TextField()
    
    question_from = models.ForeignKey("Question", on_delete = models.CASCADE)
    
  
# class tag(models.Model):
#     tag_name = models.CharField(max_length=32)
    
#     question_from = models.ForeignKey("Question", on_delete=models.CASCADE)