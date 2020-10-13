from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
class Subject(models.Model):
    subject_name=models.CharField(max_length=100)
    year=models.IntegerField(default = datetime.date.today().year)
    teacher=models.ForeignKey(User, on_delete=models.CASCADE)
    enrollment_key = models.CharField(max_length=10, default="SPIT_IT")
    def __str__(self):
        return self.subject_name+"-"+str(self.year) + "-" + str(self.teacher)

class Enroll(models.Model):
    subject = models.ForeignKey("Subject",on_delete=models.CASCADE)
    student = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.subject)+"-"+str(self.student)

class FeedbackForm(models.Model):
    type_choices=(
      ('prof', 'Professor Feedback'),
      ('course', 'Course Feedback')
    )
    sem_choices=(
        ('midsem', 'Mid semester feedback'),
        ('endsem','End semester feedback')
    )
    feedback_type = models.CharField(max_length=100,choices=type_choices)
    sem_type = models.CharField(max_length=100,choices=sem_choices)
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.subject)+"-"+ self.feedback_type + "-" + self.sem_type

class FormQuestion(models.Model):
    feedback_form = models.ForeignKey("FeedbackForm", on_delete=models.CASCADE)
    question = models.CharField(max_length=225)

    def __str__(self):
        return str(self.feedback_form)+"-Q"+ str(self.id)


class FormAnswer(models.Model):
    form_question = models.ForeignKey("FormQuestion", on_delete=models.CASCADE)
    #student = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField()

    def __str__(self):
        return str(self.form_question)+"-"+str(self.id)