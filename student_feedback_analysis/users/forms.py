from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email=forms.EmailField()
    #required is set to true, you can set it to false if you want
    class Meta:
        model=User
        fields=['username','email','first_name','last_name','password1','password2']
class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField()
    #required is set to true, you can set it to false if you want
    class Meta:
        model=User
        fields=['email','first_name','last_name']