from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Subject, FeedbackForm, FormAnswer, FormQuestion, Enroll, DraftForm, DraftQuestion
from users.decorators import unauthenticated_user, student_only, teacher_only
from django.contrib.auth.decorators import login_required
from .forms import FormFeedback, EnrollForm, StudentFeedbackForm, NewForm, NewQuestionForm, EditQuestionForm, NewDraftQuestionForm, EditDraftQuestionForm
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
from django.db.models import Q
from skills.models import Skill, SkillQuestion, SkillAnswer
import datetime
import waterfall_chart


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
        
        return render(request,'courses/formlist.html',{'tid':tid,'s':s,'f':f})
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
                return render(request,'courses/formlist.html',{'tid':tid,'s':s,'f':f})
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
            ed=[word for word,tag in pos if tag!='NNP' and tag!='NNPs'] #removing proper nouns
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
    fq=SkillQuestion.objects.all()
    fqli=[]
    i=0
    for f in fq:
        i+=1
        fqli.append(str(i)+". "+f.skill.skill_name+" -> "+f.question)
    #return render(request,'courses/formquestion.html',{'tid':tid,'sid':sid,'fid':fid,'fq':fq})
    extra_questions = fqli
    lemmatizer = WordNetLemmatizer() 
    form = StudentFeedbackForm(request.POST or None, extra=extra_questions)
    if form.is_valid():
        i=0
        q1=[]
        a1=[]
        for (question, answer) in form.extra_answers():
            i+=1
            i%=3
            
            if i==1:
                li=question.split("-> ")
                question=li[1]
           
            q1.append(question)
            a1.append(answer)
            if i==0:
                print(q1)
                print(a1)
                if a1[1]=='' and a1[2]=='':
                    pass
                else:
                                   
                    ssid=SentimentIntensityAnalyzer()
                    ss=ssid.polarity_scores(a1[1])
                    # f.sentiment=ss['compound']
                    fa=SkillAnswer(question=SkillQuestion.objects.filter(question=q1[0]).first(),yes_or_no=a1[0],student=u,answer=a1[1],tags=a1[2],sentiment=ss['compound'])
                    fa.save()
                    #print("hello")
                q1=[]
                a1=[]
        return redirect('subject-detail', sid=sid)
    return render(request, 'courses/studentform.html',{'u':u,'form':form, 'sid' : sid})

def printstudentreport(uid):
    taggedWords = []
    pos = []
    neg = []
    s = User.objects.get(id = uid)
    for ans in SkillAnswer.objects.filter(student = s):#filter(date.year == datetime.date.today().year):
        if (ans.date.year == datetime.date.today().year):
            temp = ans.tags.split(',')
            for t in temp:
                taggedWords.append(t)
        
    sentimentanalyzer=SentimentIntensityAnalyzer()
    # print(taggedWords)
    for j in taggedWords:
        if((sentimentanalyzer.polarity_scores(j))['compound']>0.3):
            pos.append(j)
        if((sentimentanalyzer.polarity_scores(j))['compound']<0.0):
            neg.append(j)
    pl = ' '.join(pos)
    nl = ' '.join(neg)

    #positive wc
    wordcloud = WordCloud(background_color='white',
    max_words=200,max_font_size=80,random_state=42).generate(pl)
    plt.figure()
    plt.tight_layout()
    fig=plt.imshow(wordcloud)
    plt.axis('off')
    fig2=plt.gcf()
    buf2=io.BytesIO()
    fig2.savefig(buf2, format="png",bbox_inches='tight')
    buf2.seek(0)
    string2=base64.b64encode(buf2.read())
    uri2=urllib.parse.quote(string2)
    #urilist2.append(uri2)
    plt.close()

    #negative wc
    wordcloud = WordCloud(background_color='white',
    max_words=200,max_font_size=80,random_state=42).generate(nl)
    wordcloud.recolor(color_func = grey_color_func)
    plt.figure()
    plt.tight_layout()
    fig=plt.imshow(wordcloud)
    plt.axis('off')
    fig3=plt.gcf()
    buf3=io.BytesIO()
    fig3.savefig(buf3, format="png",bbox_inches='tight')
    buf3.seek(0)
    string3=base64.b64encode(buf3.read())
    uri3=urllib.parse.quote(string3)
    plt.close()


    s = User.objects.get(id = uid)
    dictY = {}
    sa = SkillAnswer.objects.filter(student = s).order_by('date')
    for ans in sa:
        if ans.date.year in dictY:
            dictY[ans.date.year] += ans.sentiment
        else:
            dictY[ans.date.year] = ans.sentiment
    a = list(dictY.values())
    #a[0]=1.5
    for i in range(1,len(a)):
        a[i]=a[i]-a[i-1]

    b = [float(x) for x in list(dictY.keys())]
    #a=[0,1,2]
    print(a)
    print(b)
    buf=io.BytesIO()
    tempVar=waterfall_chart.plot(b,a).savefig(buf, format="png",bbox_inches='tight')
    #fig.show()
    buf.seek(0)
    string=base64.b64encode(buf.read())
    uri4=urllib.parse.quote(string)
    #tempVar.close()
    plt.close()


    #line
    all_s=Skill.objects.all()
    student=User.objects.get(id=uid)
    #set_subjs=set()
    s_to_print=[]
    for s in all_s: 
        diction={}
        print(s.skill_name)
        for q in SkillQuestion.objects.filter(skill=s):
            ans=SkillAnswer.objects.filter(student=student)
            ans=ans.filter(question=q)
            #ans=ans.order_by('date')
            for a in ans:
                # print(a.question.skill)
                print(a.answer)
                print(a.date)
                #print(" ")
                if a.date.year not in diction:
                    diction[a.date.year]=[0.0,0.0,0.0,0.0]
                if a.date.month <=6:
                    diction[a.date.year][0]+=a.sentiment
                    diction[a.date.year][1]+=1
                else:
                    diction[a.date.year][2]+=a.sentiment
                    diction[a.date.year][3]+=1

        diction2={}
        for stemp in sorted(diction):
            temp="June"+str(stemp)
            temp2="Dec"+str(stemp)
            try:
                diction2[temp]=diction[stemp][0]/diction[stemp][1]
            except:
                diction2[temp]=0.0
            try:
                diction2[temp2]=diction[stemp][2]/diction[stemp][3]
            except:
                diction2[temp2]=0.0
        plt.plot(list(diction2.keys()),list(diction2.values()))
        s_to_print.append(s.skill_name)
    #print(s.skill_name)
    plt.legend(s_to_print,loc="lower right")
    #print("SUbject name is ",s.subject_name)
    
    plt.tight_layout()
    plt.xlabel('Time')
    plt.ylabel('Sentiment score')
    fig5=plt.gcf()
    buf5=io.BytesIO()
    fig5.savefig(buf5, format="png",bbox_inches='tight')
    buf5.seek(0)
    string5=base64.b64encode(buf5.read())
    uri5=urllib.parse.quote(string5)
    
    plt.close()
    return uri2, uri3, uri4, uri5

@login_required
@teacher_only
def studentreport(request, sid, uid):
    # sa = SkillAnswer.objects.all()
    u=User.objects.get(id=uid)
    uri2,uri3,uri4,uri5=printstudentreport(uid)
    return render(request, 'courses/studentreport.html', {'u':u,'uri2' : uri2, 'uri3' : uri3 ,'uri4':uri4,'uri5':uri5})

@login_required
@student_only
def mystudentreport(request):
    # sa = SkillAnswer.objects.all()
    uri2,uri3,uri4,uri5=printstudentreport(request.user.id)
    return render(request, 'courses/studentreport.html', {'u':request.user, 'uri2' : uri2, 'uri3' : uri3 ,'uri4':uri4,'uri5':uri5})


@login_required
@teacher_only
def myfeedback(request,sid):
    s=Subject.objects.get(id=sid)
    f=s.feedbackform_set.all()
    d=s.draftform_set.all()

    return render(request,'courses/myfeedback.html',{'f':f,'s':s,'d':d})

def findnumber(s,ft):
    f=FeedbackForm.objects.filter(Q(subject=s) & Q(feedback_type=ft)).all()
    lif=[]
    for fi in f:
        lif.append(fi)
    fa=FormAnswer.objects.all()
    p=nt=ng=0
    pl=ngl=[]
    for fai in fa:
        if fai.form_question.feedback_form in lif:
            if fai.sentiment>0.3:
                p+=1
                #pl.append(fai)
            elif 0.1<fai.sentiment<=0.3:
                nt+=1
            else:
                ng+=1
                #ngl.append(fai)
    return p,nt,ng
def generatepie(s,feedback_type):
    f=FeedbackForm.objects.filter(Q(subject=s) & Q(feedback_type=feedback_type))
    fa=FormAnswer.objects.all()
    p=nt=ng=0
    pl=ngl=[]
    for fai in fa:
        if fai.form_question.feedback_form in f:
            if fai.sentiment>0.3:
                p+=1
                pl.append(fai)
            elif 0.1<fai.sentiment<=0.3:
                nt+=1
            else:
                ng+=1
                ngl.append(fai)
    labels = 'Positive', 'Neutral', 'Negative'
    sizes = [p,nt,ng]
    colors = ['gold', 'lightcoral','yellowgreen']
    explode = (0.1, 0, 0)  # explode 1st slice
    
    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    
    plt.axis('equal')
    plt.tight_layout()
    #plt.show()
    fig=plt.gcf()
    buf=io.BytesIO()
    fig.savefig(buf, format="png",bbox_inches='tight')
    buf.seek(0)
    string=base64.b64encode(buf.read())
    uri=urllib.parse.quote(string)
    plt.close()
    return uri,pl,ngl,sizes

def generatewordcloud(pl,is_positive):
    p=[]
    sentimentanalyzer=SentimentIntensityAnalyzer()
    for i in pl:
        a=i.processed_answer.split()
        for j in a:
            if((sentimentanalyzer.polarity_scores(j))['compound']>0.3 and is_positive):
                p.append(j)
            elif((sentimentanalyzer.polarity_scores(j))['compound']<0 and is_positive==False):
                p.append(j)
    p1=" ".join(p)
    wordcloud = WordCloud(background_color='white',
    max_words=200,max_font_size=80,random_state=42).generate(p1)
    if is_positive==False:
        wordcloud.recolor(color_func = grey_color_func)
    plt.figure()
    plt.tight_layout()
    fig=plt.imshow(wordcloud)
    plt.axis('off')
    fig2=plt.gcf()
    buf2=io.BytesIO()
    fig2.savefig(buf2, format="png",bbox_inches='tight')
    buf2.seek(0)
    string2=base64.b64encode(buf2.read())
    uri2=urllib.parse.quote(string2)
    #urilist2.append(uri2)
    plt.close()
    return uri2
def generatebar(p,nt,ng,subjects):
    ind = np.arange(len(subjects))    # the x locations for the groups
    width = 0.35       # the width of the bars: can also be len(x) sequence
    #print(ind)
    p1 = plt.barh(ind, p, width,color='g')
    p2 = plt.barh(ind, nt, width,left=p,color='y')
    p3 = plt.barh(ind, ng, width,left=np.array(p)+np.array(nt),color='r')
    
    plt.xlabel('Feedback Scores')
    plt.ylabel('Courses taught by you')
    plt.title('Scores by sentiment')
    plt.tight_layout()
    
    plt.yticks(ind, subjects)
    #plt.xticks(np.arange(0, 100, 10))
    l1=plt.legend((p1[0], p2[0],p3[0]), ('Positive','Neutral','Negative'),loc='upper center', bbox_to_anchor=(0.5, -0.15),fancybox=True, shadow=True, ncol=5)
    #l2=plt.legend(yl, fqlist,loc='best')
    plt.gca().add_artist(l1)
    #plt.gca().add_artist(l2)
    fig4=plt.gcf()
    buf4=io.BytesIO()
    fig4.savefig(buf4, format="png",bbox_inches='tight')
    buf4.seek(0)
    string4=base64.b64encode(buf4.read())
    uri4=urllib.parse.quote(string4)
    plt.close()
    return uri4

@login_required
@teacher_only
def profreport(request,sid):
    s=Subject.objects.get(id=sid)
    uri,pl,ngl,sizes=generatepie(s,"prof")
    urip=generatewordcloud(pl,True)
    urin=generatewordcloud(ngl,False)
    s=Subject.objects.filter(teacher=request.user)
    subli=[]
    pl=[]
    ntl=[]
    ngl=[]
    for si in s:
        subli.append(si.subject_name+"-"+str(si.year))
        p,nt,ng=findnumber(si,'prof')
        print(p," ",nt," ",ng)
        pl.append(p)
        ngl.append(ng)
        ntl.append(nt)
    print(pl)
    print(ntl)
    print(ngl)
    uri3=generatebar(pl,ntl,ngl,subli)
    all_s=Subject.objects.filter(teacher=request.user)
    set_subjs=set()
    for si in all_s:
        set_subjs.add(si.subject_name)
    s_to_print=[]
    for s in set_subjs:
        #s=Subject.objects.get(id=sid)
        other_s=Subject.objects.filter(subject_name=s).order_by('year')
        li=[]
        time_array=[]
        
        for si in other_s:
            summ=0
            sume=0
            te=0
            tm=0
            fm=si.feedbackform_set.all().filter(Q(sem_type="midsem") & Q(feedback_type="prof"))
            fe=si.feedbackform_set.all().filter(Q(sem_type="endsem") & Q(feedback_type="prof"))
            fa=FormAnswer.objects.all()
            for fai in fa:
                if fai.form_question.feedback_form in fm:
                    summ+=fai.sentiment
                    tm+=1
                elif fai.form_question.feedback_form in fe:
                    sume+=fai.sentiment
                    te+=1
            time_array.append("MSE"+" "+str(si.year))
            time_array.append("ESE"+" "+str(si.year))
            sm=summ/tm*100
            se=sume/te*100
            li.append(sm)
            li.append(se)
        plt.plot(time_array,li)
        s_to_print.append(s)
    plt.legend(s_to_print,loc="lower right")
    #print("SUbject name is ",s.subject_name)
    
    plt.tight_layout()
    plt.xlabel('Time')
    plt.ylabel('Sentiment score')
    fig4=plt.gcf()
    buf4=io.BytesIO()
    fig4.savefig(buf4, format="png",bbox_inches='tight')
    buf4.seek(0)
    string4=base64.b64encode(buf4.read())
    uri4=urllib.parse.quote(string4)
    total=sum(sizes)
    plt.close()
    return render(request, 'courses/profreport.html',{'uri':uri,'urip':urip,'urin':urin,'uri3':uri3,'uri4':uri4,'s':Subject.objects.get(id=sid),'total':total,'positives':sizes[0],'neutrals':sizes[1],'negatives':sizes[2]})

@login_required
@teacher_only
def coursereport(request,sid):
    s=Subject.objects.get(id=sid)
    uri,pl,ngl,sizes=generatepie(s,"course")
    urip=generatewordcloud(pl,True)
    urin=generatewordcloud(ngl,False)
    s2=Subject.objects.filter(subject_name=s.subject_name)
    subli=[]
    pl=[]
    ntl=[]
    ngl=[]
    for si in s2:
        subli.append(si.subject_name+"-"+str(si.year))
        p,nt,ng=findnumber(si,'course')
        #print(p," ",nt," ",ng)
        pl.append(p)
        ngl.append(ng)
        ntl.append(nt)
    uri3=generatebar(pl,ntl,ngl,subli)
    s=Subject.objects.get(id=sid)
    other_s=Subject.objects.filter(subject_name=s.subject_name).order_by('year')
    li=[]
    time_array=[]
    for si in other_s:
        summ=0
        sume=0
        te=0
        tm=0
        fm=si.feedbackform_set.all().filter(Q(sem_type="midsem") & Q(feedback_type="course"))
        fe=si.feedbackform_set.all().filter(Q(sem_type="endsem") & Q(feedback_type="course"))
        fa=FormAnswer.objects.all()
        for fai in fa:
            if fai.form_question.feedback_form in fm:
                summ+=fai.sentiment
                tm+=1
            elif fai.form_question.feedback_form in fe:
                sume+=fai.sentiment
                te+=1
        time_array.append("MSE"+" "+str(si.year))
        time_array.append("ESE"+" "+str(si.year))
        sm=summ/tm*100
        se=sume/te*100
        li.append(sm)
        li.append(se)
    plt.plot(time_array,li)
    s_to_print=[s.subject_name]
    #plt.legend(s_to_print,loc="lower right")
    plt.legend(s_to_print,loc='upper center', bbox_to_anchor=(0.5, -0.15),fancybox=True, shadow=True, ncol=5)
    print("SUbject name is ",s.subject_name)
    plt.xlabel('Time')
    plt.ylabel('Sentiment score')
    #plt.title('Scores by sentiment')
    plt.tight_layout()
    fig4=plt.gcf()
    buf4=io.BytesIO()
    fig4.savefig(buf4, format="png",bbox_inches='tight')
    buf4.seek(0)
    string4=base64.b64encode(buf4.read())
    uri4=urllib.parse.quote(string4)
    plt.close()
    total=sum(sizes)
    return render(request, 'courses/coursereport.html',{'uri':uri,'urip':urip,'urin':urin,'uri3':uri3,'uri4':uri4,'s':Subject.objects.get(id=sid),'total':total,'positives':sizes[0],'neutrals':sizes[1],'negatives':sizes[2]})


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
    p=0
    ng=0
    nt=0
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
    sizesfinal = [p,nt,ng]
    total=sum(sizesfinal)
    colors = ['gold', 'lightcoral','yellowgreen']
    explode = (0.1, 0, 0)  # explode 1st slice
    
    # Plot
    plt.pie(sizesfinal, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    
    plt.axis('equal')
    #plt.show()
    fig=plt.gcf()
    buf=io.BytesIO()
    fig.savefig(buf, format="png",bbox_inches='tight')
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
        fig2.savefig(buf2, format="png",bbox_inches='tight')
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
        fig3.savefig(buf3, format="png",bbox_inches='tight')
        buf3.seek(0)
        string3=base64.b64encode(buf3.read())
        uri3=urllib.parse.quote(string3)
        urilist3.append(uri3)
        plt.close()
        diction={'positive':urilist2,'negative':urilist3}
        #diction['positive']
        urilist=[]
        for i in range(len(urilist3)):
            li={}
            li['positive']=urilist2[i]
            li['negative']=urilist3[i]
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
    plt.ylabel('Questions')
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
    #plt.xticks(np.arange(0, 21, 2))
    l1=plt.legend((p1[0], p2[0],p3[0]), ('Positive','Neutral','Negative'),loc='upper center', bbox_to_anchor=(0.5, -0.15),fancybox=True, shadow=True, ncol=5)
    #l2=plt.legend(yl, fqlist,loc='best')
    plt.gca().add_artist(l1)
    #plt.gca().add_artist(l2)
    fig4=plt.gcf()
    buf4=io.BytesIO()
    fig4.savefig(buf4, format="png",bbox_inches='tight')
    buf4.seek(0)
    string4=base64.b64encode(buf4.read())
    uri4=urllib.parse.quote(string4)
    #urilist4.append(uri4)
    plt.close()
    urilistzip=zip(finalkey,urilist)
    #plt.show()
    return render(request,'courses/formreport.html',{'fi':fi,'data': uri,'l2':len(urilist2),'l3':len(urilist3),'urilist':urilist,'uri4':uri4,'finalkey':finalkey,'urilistzip':urilistzip,'total':total,'positives':sizesfinal[0],'neutrals':sizesfinal[1],'negatives':sizesfinal[2]})
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
def upload(request,sid,fid):
    s=Subject.objects.get(id=sid)
    d=DraftForm.objects.get(id=fid)
    f=FeedbackForm(feedback_type=d.feedback_type,sem_type=d.sem_type, subject=d.subject,form_name=d.form_name)
    f.save()
    df=d.draftquestion_set.all()
    for dfi in df:
        fq=FormQuestion(feedback_form=f,question=dfi.question)
        fq.save()
    d.delete()
    return redirect('myfeedback', sid=s.id)

@login_required
@teacher_only
def editdraft(request,sid,fid):
    s=Subject.objects.get(id=sid)
    f=DraftForm.objects.get(id=fid)
    fq=f.draftquestion_set.all()
    if request.method=='POST':
        form=NewDraftQuestionForm(request.POST)
        form.instance.draft_form=f
        if form.is_valid():
            form.save()
            return redirect('editdraft', sid=sid, fid=fid)
    else:
        form=NewDraftQuestionForm()
    return render(request,'courses/editdraft.html',{'s':s,'f':f,'fq':fq,'form':form})


@login_required
@teacher_only
def deletedraft(request,sid,fid):
    s=Subject.objects.get(id=sid)
    f=DraftForm.objects.get(id=fid)
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
def deletedraftquestion(request,sid,fid,fqid):
    s=Subject.objects.get(id=sid)
    f=DraftForm.objects.get(id=fid)
    fq=DraftQuestion.objects.get(id=fqid)
    fq.delete()
    return redirect('editdraft', sid=sid, fid=fid)
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

@login_required
@teacher_only
def editdraftquestion(request, sid,fid,fqid):
    s=Subject.objects.get(id=sid)
    f=DraftForm.objects.get(id=fid)
    fq=DraftQuestion.objects.get(id=fqid)
    if request.method=='POST':
        form=EditDraftQuestionForm(request.POST,instance=fq)
        form.instance.draft_form=f
        if form.is_valid():
            fq.question=form.instance.question
            fq.save()
            return redirect('editdraft', sid=sid, fid=fid)
    else:

        form=EditDraftQuestionForm(instance=fq)
    return render(request,'courses/editdraftquestion.html',{'s':s,'f':f,'fq':fq,'form':form})
