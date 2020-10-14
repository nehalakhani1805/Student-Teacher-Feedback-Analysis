from .models import Subject,FeedbackForm,FormAnswer,FormQuestion
from django.contrib.auth.models import User
import datetime

def trying():    
    s_list=['CN','CN','CN','OOP','OOP','OOP','ADS','ADS','ADS','DBMS','DBMS','DBMS','COA','COA','COA','WPL','WPL','WPL','DAA','DAA','DAA']
    count=0
    for u in User.objects.all():
        if u.groups.all()[0].name=='teacher':
            for i in range(3):
                s=Subject(subject_name=s_list[count],year=datetime.date.today().year - i,teacher=u)
                s.save()
                count+=1
    i=0
    for u in User.objects.all():
        if i<2:
            if u.groups.all()[0].name=='teacher':
                i+=1
                for j in range(3):
                    s=Subject(subject_name=s_list[count],year=datetime.date.today().year - j,teacher=u)
                    s.save()
                    count+=1
        else:
            break
def trying2():
    # questions_t=['How good were the concepts of the teacher?','How did you find the teaching style?','How interactive is the teacher?','Any other comments/grievances?']
    # questions_c=['How useful was the course?','How is the course grading','What was the difficulty of the course?','Any other comments/grievances']
    for s in Subject.objects.all():
        f=FeedbackForm(feedback_type="prof",sem_type="midsem",subject=s)
        f.save()
        f=FeedbackForm(feedback_type="prof",sem_type="endsem",subject=s)
        f.save()
        f=FeedbackForm(feedback_type="course",sem_type="midsem",subject=s)
        f.save()
        f=FeedbackForm(feedback_type="course",sem_type="endsem",subject=s)
        f.save()
    #FeedbackForm.objects.all().delete()
def trying3():
    # questions_t=['How good were the concepts of the teacher?','How did you find the teaching style?','How interactive is the teacher?','Any other comments/grievances?']
    # questions_c=['How useful was the course?','How is the course grading','What was the difficulty of the course?','Any other comments/grievances']
    # for f in FeedbackForm.objects.all():
    #     if f.feedback_type=='course':
    #         for i in range(4):
    #             f2=FormQuestion(feedback_form=f,question=questions_c[i])
    #             f2.save()
    #     else:
    #         for i in range(4):
    #             f2=FormQuestion(feedback_form=f,question=questions_t[i])
    #             f2.save()
    FormQuestion.objects.all().delete()


