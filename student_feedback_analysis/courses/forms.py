from django import forms
from django.db import models
from .models import Subject, FeedbackForm, FormQuestion
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

class StudentFeedbackForm(forms.ModelForm):
    #enrollment_key=forms.CharField(widget=forms.PasswordInput)
    #required is set to true, you can set it to false if you want
    class Meta:
        model=SkillAnswer
        fields=['question','yes_or_no','answer']


class NewForm(forms.ModelForm):
    #enrollment_key=forms.CharField(widget=forms.PasswordInput)
    #required is set to true, you can set it to false if you want
    class Meta:
        model=FeedbackForm
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
        