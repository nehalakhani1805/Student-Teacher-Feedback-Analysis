# Create your views here.
from django.shortcuts import render,redirect
#from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, student_only, teacher_only
from django.contrib.auth.models import Group, User
from courses import data

@login_required
def home(request):
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
        if group == 'teacher':
            return render(request, 'users/teacher_home.html')
        if group == 'student':
            li=[]
            for u in User.objects.all():
                if u.groups.all()[0].name=='teacher':
                    li.append(u)
            return render(request, 'users/student_home.html',{'li':li})
@unauthenticated_user
def register(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            user=form.save() #this saves the details to the db
            group=Group.objects.get(name="student")
            user.groups.add(group)
            username=form.cleaned_data.get('username') 
            #not form.username.data
            messages.success(request,f'Welcome {username}')
            #note the single braces
            return redirect ('home')#remember to import redirect
    else:
        form=UserRegisterForm()
    return render(request, 'users/register.html',{'form':form})

@login_required
def profile(request):
    if request.method=='POST':
        form=UserUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save() #this saves the details to the db
            #username=form.cleaned_data.get('username') 
            #not form.username.data
            messages.success(request,f'Profile updated successfully!')
            return redirect ('profile')#remember to import redirect
    else:
        form=UserUpdateForm(instance=request.user)
    return render(request, 'users/profile.html',{'form':form})



@login_required
@teacher_only
def test(request):
    data.trying4()
    return render(request,'users/home.html')
