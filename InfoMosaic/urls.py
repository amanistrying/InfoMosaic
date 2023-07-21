from django.contrib import admin
from django.urls import path, include
from InfoMosaic import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('serviceProvider/signup/', views.spSignUp, name='serviceProviderSignUp'),
    path('serviceProvide/login', views.spsignedup, name='serviceProviderLogIn'),
    path('serviceProvider/login/', views.splogin, name='home'),
    path('serviceProvider/loginpage/', views.login, name='Login'),
    path('login/main/', views.main, name='main'),
    path('user/login/', views.home, name='login'),
    path('user/signIn/', views.signIn, name='signUp'),
    path('user/signup/', views.usersignUp, name='userSignUp'),
    path('serviceProvider/home', views.sp_home, name='sphome'),
    path('InfoMosaic/', views.welcome, name='welcome'),
    path('user/', views.user, name='user'),
    path('serviceProvider/', views.sp, name='edit'),
    path('serviceProvider/login/', views.logout, name='logout')
]
