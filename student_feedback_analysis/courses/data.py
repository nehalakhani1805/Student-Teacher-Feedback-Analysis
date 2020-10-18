from .models import Subject,FeedbackForm,FormAnswer,FormQuestion
from skills.models import SkillAnswer
from django.contrib.auth.models import User
import datetime
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
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer






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
    questions_t=['How good were the concepts of the teacher?','How did you find the teaching style?','How interactive is the teacher?','Any other comments/grievances?']
    questions_c=['How useful was the course?','How is the course grading','What was the difficulty of the course?','Any other comments/grievances']
    counter=0
    counter2=0
    for f in FeedbackForm.objects.all():
        if f.feedback_type=='course':
            print(counter,"course ",f.subject.subject_name)
            for i in range(4):
                print(counter2)
                counter2+=1
                f2=FormQuestion(feedback_form=f,question=questions_c[i])
                f2.save()
        else:
            print(counter,"prof ",f.subject.subject_name)
            for i in range(4):
                print(counter2)
                counter2+=1
                f2=FormQuestion(feedback_form=f,question=questions_t[i])
                f2.save()
        counter+=1
    #FormQuestion.objects.all().delete()

def trying4():
    count=0
    ind=np.arange(22477)
    df=pd.read_csv('C:/Users/NEHA LAKHANI/Documents/student_feedback/reviews.csv')
    #print(df['Review'])
    df2=df['Review']
    df2['Id']=ind
    #header=['Review']
    #df2.to_csv('C:/Users/NEHA LAKHANI/Documents/student_feedback/reviews2.csv',header=header)
    #df2.sort_index()
    #df2=df2.astype(str)
    #print(df2.head())
    #print(str(df2['Id']))
    #print(df.iloc[0]['Review'])
    counter=0
    for f in FormQuestion.objects.all():
        for i in range(10):
            f2=FormAnswer(form_question=f,answer=df.iloc[counter]['Review'])
            f2.save()
            counter+=1

    #     if count<5:
    #         #for f in FormQuestion.objects.all():
    #         print(i)
    #         print(count)
    #         count+=1
    #     else:
    #         break
    



    # for f in FormQuestion.objects.all():
    #     for i in range(10):


def trying5():
    sa=SkillAnswer.objects.all()
    lemmatizer = WordNetLemmatizer()
    #i=1000
    for f in sa:  
        
        # i+=1
        #remove punctuation
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(f.answer)
        final=' '.join(tokens)


        #remove non english words
        a1=" ".join(w for w in nltk.wordpunct_tokenize(final)if w.lower() in words or not w.isalpha())

        #remove proper nouns
        tokenized2 = nltk.word_tokenize(a1)
        tokenized=[lemmatizer.lemmatize(w) for w in tokenized2]
        temp=' '.join(tokenized)
        #tokenized=[ps.stem(w) for w in tokenized3]
        pos=nltk.tag.pos_tag(tokenized)
        ed=[word for word,tag in pos if tag!='NNP' and tag!='NNPs']#removing proper nouns
        end=' '.join(ed)

        #remove stop words
        # en=[i for i in word_tokenize(end.lower()) if i not in stop] 
        # final=' '.join(en)

        #using vader classfiers
        f.processed_answer = end
        sid=SentimentIntensityAnalyzer()
        ss=sid.polarity_scores(f.processed_answer)
        f.sentiment=ss['compound']
        #f.processed_answer=final
        f.save()
    # else:
    #     break

