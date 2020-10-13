from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Skill(models.Model):
    skill_name = models.CharField(max_length=100)

    def __str__(self):
        return self.skill_name


class SkillQuestion(models.Model):
    skill=models.ForeignKey("Skill",on_delete=models.CASCADE)
    question = models.CharField(max_length=225)

    def __str__(self):
        return str(self.skill)+"-Q"+str(self.id)


class SkillAnswer(models.Model):
    question=models.ForeignKey("SkillQuestion",on_delete=models.CASCADE)
    yes_or_no = models.BooleanField(default=True)
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    answer = models.TextField(max_length=225)

    def __str__(self):
        return str(self.question)+"-A"+str(self.id)

