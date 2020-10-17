from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Subject, FeedbackForm, FormAnswer, FormQuestion, Enroll
from users.decorators import unauthenticated_user, student_only, teacher_only
from django.contrib.auth.decorators import login_required
from .forms import FormFeedback, EnrollForm, StudentFeedbackForm, NewForm, NewQuestionForm, EditQuestionForm
from django.contrib import messages
import pandas as pd
import nltk
from wordcloud import WordCloud, STOPWORDS
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
words = set(nltk.corpus.words.words())
from nltk.tokenize import RegexpTokenizer
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import urllib,base64
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

# Create your views here.
@login_required
@student_only
def subjects(request,tid):
    t=User.objects.get(id=tid)
    s=t.subject_set.all().order_by('-year')
    return render(request,'courses/subjects.html',{'s':s,'tid':tid})

@login_required
@student_only
def subjectfeedback(request,tid,sid):
    s=Subject.objects.get(id=sid)
    u=User.objects.get(id=request.user.id)
    e=Enroll.objects.all()
    flag=False
    for ei in e:
        if ei.student == u and ei.subject == s:
            flag=True
    f=s.feedbackform_set.all().order_by('-sem_type')
    if flag==True:
        #t=User.objects.get(id=tid)
        
        return render(request,'courses/formlist.html',{'tid':tid,'sid':sid,'f':f})
    else:
        if request.method=='POST':
            form=EnrollForm(request.POST)
            if form.is_valid() and form.cleaned_data.get('enrollment_key') == s.enrollment_key :
                #user=form.save() #this saves the details to the db
                #group=Group.objects.get(name="student")
                #user.groups.add(group)
                #username=form.cleaned_data.get('username') 
                #not form.username.data
                e = Enroll(subject=s,student=u)
                e.save()
                messages.success(request,f'Welcome')
                #note the single braces
                return render(request,'courses/formlist.html',{'tid':tid,'sid':sid,'f':f})
            else:
                messages.warning(request,f'Incorrect enrollment key')
        else:
    
            form=EnrollForm()
        return render(request, 'courses/enrollform.html',{'form':form})

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
    lemmatizer = WordNetLemmatizer()
    form = FormFeedback(request.POST or None, extra=extra_questions)
    if form.is_valid():
        for (question, answer) in form.extra_answers():
            #save_answer(request, question, answer)
            print(question)
            print(answer)
            f=fq.filter(question=question).first()
            fa=FormAnswer(form_question=f,answer=answer)
            #remove punctuation

            tokenizer = RegexpTokenizer(r'\w+')
            tokens = tokenizer.tokenize(fa.answer)
            final=' '.join(tokens)


            #remove non english words
            a1=" ".join(w for w in nltk.wordpunct_tokenize(final)if w.lower() in words or not w.isalpha())

            #remove proper nouns
            tokenized2 = nltk.word_tokenize(a1)
            tokenized=[lemmatizer.lemmatize(w) for w in tokenized2]
            #tokenized=[ps.stem(w) for w in tokenized3]
            pos=nltk.tag.pos_tag(tokenized)
            ed=[word for word,tag in pos if tag!='NNP' and tag!='NNPs']#removing proper nouns
            end=' '.join(ed)

            #remove stop words
            # en=[i for i in word_tokenize(end.lower()) if i not in stop] 
            # final=' '.join(en)

            #using vader classfiers
            sid=SentimentIntensityAnalyzer()
            ss=sid.polarity_scores(final)
            fa.sentiment=ss['compound']
            fa.processed_answer=final
            fa.save()
            #fa.save()

        return redirect("home")

    return render(request, "courses/formquestion.html", {'tid':tid,'sid':sid,'fid':fid,'form': form})

@login_required
@teacher_only
def subjectdetail(request, sid):
    s=Subject.objects.get(id=sid)
    e=s.enroll_set.all()
    li=[]
    for ei in e:
        u=User.objects.get(id=ei.student.id)
        li.append(u)
    return render(request, 'courses/subjectdetail.html',{'s':s,'li':li})

@login_required
@teacher_only
def studentfeedback(request, sid, uid):
    u=User.objects.get(id=uid)
    if request.method=='POST':
        form=StudentFeedbackForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False) #this saves the details to the db
            #username=form.cleaned_data.get('username') 
            #not form.username.data
            obj.student=u
            obj.save()
            print(form.cleaned_data.get('question'))
            messages.success(request,f'Your response has been recorded!')
            return render(request, 'courses/studentform.html',{'uid':uid,'form':form})
    else:
        form=StudentFeedbackForm()
    #return render(request, 'users/profile.html',{'form':form})
    return render(request, 'courses/studentform.html',{'u':u,'form':form})

@login_required
@teacher_only
def myfeedback(request,sid):
    s=Subject.objects.get(id=sid)
    f=s.feedbackform_set.all()

    return render(request,'courses/myfeedback.html',{'f':f,'s':s})

@login_required
@teacher_only
def newform(request,sid):
    s=Subject.objects.get(id=sid)
    if request.method=='POST':
        form=NewForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False) #this saves the details to the db
            #username=form.cleaned_data.get('username') 
            #not form.username.data
            obj.subject=s
            obj.save()
            #print(form.cleaned_data.get('question'))
            messages.success(request,f'Your response has been recorded!')
            return redirect('myfeedback', sid=s.id)
    else:
        form=NewForm()
    #return render(request, 'users/profile.html',{'form':form})
    #return render(request, 'courses/studentform.html',{'u':u,'form':form})
    return render(request,'courses/newform.html',{'s':s,'form':form})

def grey_color_func(word, font_size, position,orientation,random_state=None, **kwargs):
    return("hsl(0,100%%,%d%%)" % np.random.randint(35,70))

@login_required
@teacher_only
def formreport(request,sid,fid):
    fa=FormAnswer.objects.all()
    p=ng=nt=0
    fi=FeedbackForm.objects.get(id=fid)
    fq=fi.formquestion_set.first()
    pl=ngl=ntl={}
    numbers={}
    #pie chart
    for fai in fa:
        if fai.form_question.feedback_form.id == fid:
            
            if fai.sentiment > 0.3:
                p+=1
                if fai.form_question.question not in pl:
                    pl[fai.form_question.question]=[fai]
                else:
                    pl[fai.form_question.question].append(fai)
                if fai.form_question.question not in numbers:
                    numbers[fai.form_question.question]=[1,0,0]
                else:
                    numbers[fai.form_question.question][0]+=1
            elif 0.1<fai.sentiment<=0.3:
                nt+=1
                if fai.form_question.question not in pl:
                    pl[fai.form_question.question]=[fai]
                else:
                    pl[fai.form_question.question].append(fai)
                if fai.form_question.question not in numbers:
                    numbers[fai.form_question.question]=[0,1,0]
                else:
                    numbers[fai.form_question.question][1]+=1
            else:
                ng+=1
                if fai.form_question.question not in pl:
                    pl[fai.form_question.question]=[fai]
                else:
                    pl[fai.form_question.question].append(fai)
                if fai.form_question.question not in numbers:
                    numbers[fai.form_question.question]=[0,0,1]
                else:
                    numbers[fai.form_question.question][2]+=1
    print("hi")
    print(len(pl.keys()))
    print(len(ngl.keys()))
    labels = 'Positive', 'Neutral', 'Negative'
    sizes = [p,nt,ng]
    colors = ['gold', 'lightcoral','yellowgreen']
    explode = (0.1, 0, 0)  # explode 1st slice
    
    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    
    plt.axis('equal')
    #plt.show()
    fig=plt.gcf()
    buf=io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    string=base64.b64encode(buf.read())
    uri=urllib.parse.quote(string)
    plt.close()
    
    #positive wordcloud
    urilist2=[]
    for pli in pl:
        p=[]
        sentimentanalyzer=SentimentIntensityAnalyzer()
        for i in pl[pli]:
            a=i.processed_answer.split()
            for j in a:
                if((sentimentanalyzer.polarity_scores(j))['compound']>0.3):
                    p.append(j)
        p1=" ".join(p)
        wordcloud = WordCloud(background_color='white',
        max_words=200,max_font_size=80,random_state=42).generate(p1)
        plt.figure()
        fig=plt.imshow(wordcloud)
        plt.axis('off')
        fig2=plt.gcf()
        buf2=io.BytesIO()
        fig2.savefig(buf2, format="png")
        buf2.seek(0)
        string2=base64.b64encode(buf2.read())
        uri2=urllib.parse.quote(string2)
        urilist2.append(uri2)
        plt.close()

    #negative wordcloud
    urilist3=[]
    for ngli in ngl:
        p=[]
        for i in ngl[ngli]:
            a=i.processed_answer.split()
            for j in a:
                if((sentimentanalyzer.polarity_scores(j))['compound']<0.0):
                    p.append(j)
        p1=" ".join(p)
        wordcloud = WordCloud(background_color='white',
        max_words=20,max_font_size=80,random_state=42).generate(p1)
        wordcloud.recolor(color_func = grey_color_func)
        plt.figure()
        fig=plt.imshow(wordcloud)
        plt.axis('off')
        fig3=plt.gcf()
        buf3=io.BytesIO()
        fig3.savefig(buf3, format="png")
        buf3.seek(0)
        string3=base64.b64encode(buf3.read())
        uri3=urllib.parse.quote(string3)
        urilist3.append(uri3)
        plt.close()
        diction={'positive':urilist2,'negative':urilist3}
        #diction['positive']
        urilist=[]
        for i in range(len(urilist3)):
            li=[]
            li.append(urilist2[i])
            li.append(urilist3[i])
            urilist.append(li)

    #horizontal stacked bar graph
    p=[x[0] for x in numbers.values()]
    nt=[x[1] for x in numbers.values()]
    ng=[x[2] for x in numbers.values()] 
    print(numbers)   
    print(p)
    ind = np.arange(len(urilist3))    # the x locations for the groups
    width = 0.35       # the width of the bars: can also be len(x) sequence
    #print(ind)
    p1 = plt.barh(ind, p, width,color='g')
    p2 = plt.barh(ind, nt, width,left=p,color='y')
    p3 = plt.barh(ind, ng, width,left=np.array(p)+np.array(nt),color='r')
    
    plt.xlabel('Feedback Scores')
    plt.title('Scores by sentiment')
    plt.tight_layout()
    f=FeedbackForm.objects.get(id=fid)
    fq=f.formquestion_set.all()
    fqlist=[]
    for fqi in fq:
        fqlist.append(fqi.question)
    yl=[]
    finalkey=[]
    for i in range(len(urilist3)):
        yl.append("Q"+str(i+1))
        finalkey.append("Q"+str(i+1)+"-"+fqlist[i])
    plt.yticks(ind, yl)
    plt.xticks(np.arange(0, 20, 4))
    l1=plt.legend((p1[0], p2[0],p3[0]), ('Positive','Neutral','Negative'))
    #l2=plt.legend(yl, fqlist,loc='best')
    plt.gca().add_artist(l1)
    #plt.gca().add_artist(l2)
    fig4=plt.gcf()
    buf4=io.BytesIO()
    fig4.savefig(buf4, format="png")
    buf4.seek(0)
    string4=base64.b64encode(buf4.read())
    uri4=urllib.parse.quote(string4)
    #urilist4.append(uri4)
    plt.close()

    #plt.show()
    return render(request,'courses/formreport.html',{'data': uri,'l2':len(urilist2),'l3':len(urilist3),'urilist':urilist,'uri4':uri4,'finalkey':finalkey})
    #return render(request,'courses/test.html')




@login_required
@teacher_only
def editform(request,sid,fid):
    s=Subject.objects.get(id=sid)
    f=FeedbackForm.objects.get(id=fid)
    fq=f.formquestion_set.all()
    if request.method=='POST':
        form=NewQuestionForm(request.POST)
        form.instance.feedback_form=f
        if form.is_valid():
            form.save()
            return redirect('editform', sid=sid, fid=fid)
    else:
        form=NewQuestionForm()
    return render(request,'courses/editform.html',{'s':s,'f':f,'fq':fq,'form':form})

@login_required
@teacher_only
def deleteform(request,sid,fid):
    s=Subject.objects.get(id=sid)
    f=FeedbackForm.objects.get(id=fid)
    #fq=f.formquestion_set.all()
    f.delete()
    return redirect('myfeedback', sid=s.id)

@login_required
@teacher_only
def deletequestion(request,sid,fid,fqid):
    s=Subject.objects.get(id=sid)
    f=FeedbackForm.objects.get(id=fid)
    fq=FormQuestion.objects.get(id=fqid)
    fq.delete()
    return redirect('editform', sid=sid, fid=fid)

@login_required
@teacher_only
def editquestion(request, sid,fid,fqid):
    s=Subject.objects.get(id=sid)
    f=FeedbackForm.objects.get(id=fid)
    fq=FormQuestion.objects.get(id=fqid)
    if request.method=='POST':
        form=EditQuestionForm(request.POST,instance=fq)
        form.instance.feedback_form=f
        if form.is_valid():
            fq.question=form.instance.question
            fq.save()
            return redirect('editform', sid=sid, fid=fid)
    else:

        form=EditQuestionForm(instance=fq)
    return render(request,'courses/editquestion.html',{'s':s,'f':f,'fq':fq,'form':form})
