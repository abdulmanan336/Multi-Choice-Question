from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Quiz(models.Model):
    title = models.CharField( max_length=50)
    description = models.TextField()
    
    def __str__(self) -> str:
        return self.title
    
class Question(models.Model):
    quiz = models.ForeignKey( Quiz, on_delete=models.CASCADE,)
    content = models.CharField( max_length=350)
    
    def __str__(self) -> str:
        return self.content
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name="choices")
    content = models.CharField( max_length=350)
    correct = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.content
    
class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.user.username}`s response to {self.choice.question.content}"
    