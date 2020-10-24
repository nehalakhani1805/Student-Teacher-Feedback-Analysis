from .models import Subject,FeedbackForm,FormAnswer,FormQuestion
from skills.models import SkillAnswer, SkillQuestion, Skill
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
from sklearn.feature_extraction.text import TfidfTransformer 
from sklearn.feature_extraction.text import CountVectorizer 





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
    print('in t5')
    sa=SkillAnswer.objects.all()
    lemmatizer = WordNetLemmatizer()
    #i=1000
    for f in sa:              
        #using vader classfiers
        sid=SentimentIntensityAnalyzer()
        ss=sid.polarity_scores(f.answer)
        f.sentiment=ss['compound']
        f.save()
    #tf - idf
    # skillArr = [x for x in Skill.objects.all()]
    # for i in Skill.objects.all():
    #     for q in SkillQuestion.objects.filter(skill = i):
    #         docs = []
    #         for ans in SkillAnswer.objects.filter(question = q):
    #             docs.append(ans.answer)
    #         # print(docs)
    #         cv = CountVectorizer()
    #         word_count_vec = cv.fit_transform(docs)
    #         tfidf_transformer = TfidfTransformer(smooth_idf=True,use_idf=True) 
    #         tfidf_transformer.fit(word_count_vec)
    #         count_vec = cv.transform(docs)
    #         tf_idf_vec = tfidf_transformer.transform(count_vec)
    #         feature_names = cv.get_feature_names() 
    #         first_document_vector = tf_idf_vec[0] 
    #         # doc_mat = tf_idf_vec[0]
    #         df = pd.DataFrame(first_document_vector.T.todense(), index=feature_names, columns=["tfidf"]) 
    #         df.sort_values(by = ["tfidf"], ascending = False, inplace = True)
    #         for ans in SkillAnswer.objects.filter(question = q):
    #             ii = 0
    #             nl = []
    #             for word in df.index:
    #                 if word not in set(stopwords.words('english')):
    #                     ii += 1
    #                     nl.append(word)
    #                 if ii >= 2:
    #                     break
    #             ans.processed_answer = ' '.join(nl)
    #             ans.save()
def trying6():
    f=FeedbackForm.objects.all()
    for fi in f:
        fi.form_name = str(fi.get_feedback_type_display())+" "+str(fi.get_sem_type_display())
        #fi.form_name = str(fi.feedback_type)+" "+str(fi.sem_type)
        fi.save()
            


    
