from django.shortcuts import render,redirect
from . import models
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

# Create your views here.

def signin(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username , password=password)
        if user:
            login(request, user)
            return redirect('main')
        else:
            return render(request,'user.html', {'error_message': 'Invalid username or password '})
    
    if request.user.is_authenticated:
        return redirect('main')
    else:
        return render(request,'user.html')

def user(request):
    return render(request,'user.html')

def signout(request):
    logout(request)
    return redirect('main')


def signup(request):
    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        try:
            user = User.objects.create_user(username=username,email=email,password=password)
            login(request,user)
            return redirect('main')
        except IntegrityError:
            return render(request , 'user.html', {'error_message': 'Username doesnot exsit '})

def main(request):
    quizes = models.Quiz.objects.order_by("-id").all()
    ctx = {
        'quizes':quizes,
    }
    return render(request,'main.html',ctx)
    

def quiz(request,id):
    if request.user.is_authenticated:
        quiz= models.Quiz.objects.get(id=id)
        answered_question_id= models.Response.objects.filter(user=request.user,quiz=quiz).values_list("question__id",flat=True)
        unanswered_question = models.Question.objects.filter(quiz=quiz).exclude(id__in=answered_question_id)
        random_question= unanswered_question.order_by('?').first()
    else:
        return render(request,'user.html')
    
    ctx = {
        'question':random_question,
    }
    return render(request,'quiz.html',ctx)

def submit(request):
    id = request.POST.get("choice")
    choice = models.Choice.objects.get(id=id)
    print(choice)
    print(choice.question)
    print(choice.question.quiz)
    models.Response.objects.create(user=request.user,choice=choice,question=choice.question,quiz=choice.question.quiz)
    
    return redirect('quiz',id=choice.question.quiz.id)

def result(request):
    quiz_id= models.Response.objects.filter(user=request.user).values("quiz")
    uniqe_quizzes= models.Quiz.objects.filter(id__in=quiz_id)
    for quiz in uniqe_quizzes:
        total_responces=models.Response.objects.filter(user=request.user,quiz=quiz).count()
        correct_responces=models.Response.objects.filter(user=request.user,quiz=quiz,choice__correct=True).count()
        quiz.response_rate = (correct_responces / total_responces) * 100
    ctx ={
        'quizzes':uniqe_quizzes,
    } 
    return render(request,'result.html',ctx)

def result_quiz(request,id):
    quiz = models.Quiz.objects.get(id=id)
    responces = models.Response.objects.filter(user=request.user,quiz=quiz)
    total_responces =responces.count()
    ctx ={
        'quiz':quiz,
        'responces':responces,
       'total_responces':total_responces,
    }
    return render(request,'check_result.html',ctx)
