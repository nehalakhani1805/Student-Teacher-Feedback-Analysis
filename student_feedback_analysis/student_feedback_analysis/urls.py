"""student_feedback_analysis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views as users_views
from django.contrib.auth import views as auth_views
from courses import views as courses_views

urlpatterns = [
    path('',users_views.home,name='home'),
    path('admin/', admin.site.urls),
    path('register/',users_views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('profile/',users_views.profile,name='profile'),
    path('test/',users_views.test,name='test'),
    path('subjects/<int:tid>/',courses_views.subjects,name='subjects'),
    path('subjects/<int:tid>/<int:sid>/',courses_views.subjectfeedback,name='subject-feedback'),
    path('subjects/<int:tid>/<int:sid>/<int:fid>/',courses_views.feedbackdetail,name='feedback-detail'),
    path('subjectdetail/<int:sid>/',courses_views.subjectdetail,name='subject-detail'),
    path('subjectdetail/<int:sid>/<int:uid>/studentfeedback/',courses_views.studentfeedback,name='student-feedback'),
    path('subjectdetail/<int:sid>/<int:uid>/studentreport/',courses_views.studentreport,name='student-report'),
    path('subjectdetail/<int:sid>/myfeedback/',courses_views.myfeedback,name='myfeedback'),
    path('subjectdetail/<int:sid>/myfeedback/profreport',courses_views.profreport,name='profreport'),
    path('subjectdetail/<int:sid>/myfeedback/coursereport',courses_views.coursereport,name='coursereport'),
    path('subjectdetail/<int:sid>/myfeedback/newform/',courses_views.newform,name='newform'),
    path('subjectdetail/<int:sid>/myfeedback/<int:fid>/formreport/',courses_views.formreport,name='formreport'),
    path('subjectdetail/<int:sid>/myfeedback/<int:fid>/deleteform/',courses_views.deleteform,name='deleteform'),
    path('subjectdetail/<int:sid>/myfeedback/<int:fid>/editform/',courses_views.editform,name='editform'),
    path('subjectdetail/<int:sid>/myfeedback/<int:fid>/editform/<int:fqid>/deletequestion/',courses_views.deletequestion,name='deletequestion'),
    path('subjectdetail/<int:sid>/myfeedback/<int:fid>/editform/<int:fqid>/editquestion/',courses_views.editquestion,name='editquestion'),
]
