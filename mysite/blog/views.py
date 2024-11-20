from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from .models import Contacts

def home(request):
#    return HttpResponse("Добро пожаловать на мой сайт!")
    return render(request, 'blog/home.html')

# Представление для страницы "О нас"
def about(request):
    return render(request, 'blog/about.html')

def test(request):
    return render(request, 'blog/test.html')

from django.contrib import messages

def send_review(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Сохранение данных
            Contacts.objects.create(
                name=form.cleaned_data['name'],
                number=form.cleaned_data['number'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            # Сообщение об успешной отправке
            messages.success(request, "Заявка успешно отправлена!")
            return redirect('/about/')
        else:
            messages.error(request, "Ошибка отправки формы. Проверьте введенные данные.")
    else:
        form = ContactForm()

    return render(request, 'blog/about.html', {'form': form})

