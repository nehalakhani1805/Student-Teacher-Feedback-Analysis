from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Subject, FeedbackForm, FormAnswer, FormQuestion
from users.decorators import unauthenticated_user, student_only, teacher_only
from django.contrib.auth.decorators import login_required
from .forms import FormFeedback

# Create your views here.
@login_required
@student_only
def subjects(request,tid):
    t=User.objects.get(id=tid)
    s=t.subject_set.all()
    return render(request,'courses/subjects.html',{'s':s,'tid':tid})

@login_required
@student_only
def subjectfeedback(request,tid,sid):
    s=Subject.objects.get(id=sid)
    #t=User.objects.get(id=tid)
    f=s.feedbackform_set.all()
    return render(request,'courses/formlist.html',{'tid':tid,'sid':sid,'f':f})

@login_required
@student_only
def feedbackdetail(request,tid,sid,fid):
    f=FeedbackForm.objects.get(id=fid)
    #t=User.objects.get(id=tid)
    fq=f.formquestion_set.all()
    fqli=[]
    for f in fq:
        fqli.append(f.question)
    #return render(request,'courses/formquestion.html',{'tid':tid,'sid':sid,'fid':fid,'fq':fq})
    extra_questions = fqli
    form = FormFeedback(request.POST or None, extra=extra_questions)
    if form.is_valid():
        for (question, answer) in form.extra_answers():
            #save_answer(request, question, answer)
            print(question)
            print(answer)
            f=fq.filter(question=question).first()
            fa=FormAnswer(form_question=f,answer=answer)
            fa.save()
        return redirect("home")

    return render(request, "courses/formquestion.html", {'tid':tid,'sid':sid,'fid':fid,'form': form})