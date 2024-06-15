from django.contrib import admin
from django.urls import path
from multiple_choise  import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user', views.user,name='user'),
    path('signin', views.signin,name='signin'),
    path('signup', views.signup,name='signup'),
    path('signout', views.signout,name='signout'),
    path('',views.main,name='main'),
    path('quiz/<id>',views.quiz,name='quiz'),
    path('submit',views.submit,name='submit'),
    path('result',views.result,name='result'),
    path('result_quiz/<id>',views.result_quiz,name='result_quiz'),
]
