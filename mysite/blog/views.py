from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home(request):
#    return HttpResponse("Добро пожаловать на мой сайт!")
    return render(request, 'home.html')

# Представление для страницы "О нас"
def about(request):
    return render(request, 'about.html')

def home(request):
    context = {'welcome_message': 'Добро пожаловать на наш сайт!'}
    return render(request, 'home.html', context)
