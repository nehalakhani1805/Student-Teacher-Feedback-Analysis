from django import forms
from django.db import models
from .models import Subject, FeedbackForm, FormQuestion, DraftForm, DraftQuestion
from skills.models import SkillAnswer
class FormFeedback(forms.Form):
    #username = forms.CharField(max_length=30)
    #password1 = forms.CharField(widget=forms.PasswordInput)
    #password2 = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(FormFeedback, self).__init__(*args, **kwargs)

        for i, question in enumerate(extra):
            self.fields['custom_%s' % i] = forms.CharField(label=question,widget=forms.Textarea)
            #self.fields['custom_%s' % i] = models.TextField(label=question)
            #self.fields['custom_%s' % i] = forms.CharField(label=question,widget=forms.Textarea)
    def extra_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield (self.fields[name].label, value)

class EnrollForm(forms.ModelForm):
    enrollment_key=forms.CharField(widget=forms.PasswordInput)
    #required is set to true, you can set it to false if you want

    class Meta:
        model=Subject
        fields=['enrollment_key']

class StudentFeedbackForm(forms.Form):
    #enrollment_key=forms.CharField(widget=forms.PasswordInput)
    #required is set to true, you can set it to false if you want
    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(StudentFeedbackForm, self).__init__(*args, **kwargs)

        for i, question in enumerate(extra):
            #self.label="hello"
            self.fields['custom_%s' % i] = forms.BooleanField(label=question,required=False)
            self.fields['custom2_%s' % i] = forms.CharField(label="Answer",required=False)
            #self.fields['custom_%s' % i] = models.TextField(label=question)
            
            self.fields['custom3_%s' % i] = forms.CharField(label='Tags',required=False)
    def extra_answers(self):
        for name, value in self.cleaned_data.items():
            a=b=c=d=e=f=None
            #if name.startswith('custom_') or name.startswith('custom2_') or name.startswith('custom3_'):
            if name.startswith('custom_'):
                yield(self.fields[name].label, value)
            if name.startswith('custom2_'):
                yield(self.fields[name].label, value)
            if name.startswith('custom3_'):
                yield(self.fields[name].label, value)
                


class NewForm(forms.ModelForm):
    #enrollment_key=forms.CharField(widget=forms.PasswordInput)
    #required is set to true, you can set it to false if you want
    class Meta:
        model=DraftForm
        fields=['form_name','feedback_type','sem_type']
class NewQuestionForm(forms.ModelForm):
    #enrollment_key=forms.CharField(widget=forms.PasswordInput)
    #required is set to true, you can set it to false if you want
    class Meta:
        model=FormQuestion
        fields=['question']
class EditQuestionForm(forms.ModelForm):
    #enrollment_key=forms.CharField(widget=forms.PasswordInput)
    #required is set to true, you can set it to false if you want
    class Meta:
        model=FormQuestion
        fields=['question']

class NewDraftQuestionForm(forms.ModelForm):
    #enrollment_key=forms.CharField(widget=forms.PasswordInput)
    #required is set to true, you can set it to false if you want
    class Meta:
        model=DraftQuestion
        fields=['question']
class EditDraftQuestionForm(forms.ModelForm):
    #enrollment_key=forms.CharField(widget=forms.PasswordInput)
    #required is set to true, you can set it to false if you want
    class Meta:
        model=DraftQuestion
        fields=['question']