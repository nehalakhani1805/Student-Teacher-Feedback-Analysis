from django import forms
from django.db import models
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