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
]
