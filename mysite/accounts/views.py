from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import ProfileForm, UserLoginForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required

def accounts(request):
    return render(request, 'accounts/accounts_form.html')


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, f"{username}, Вы успешно вошли в систему.")
                return HttpResponseRedirect(reverse('blog:home'))
            else:
                messages.error(request, "Неверное имя пользователя или пароль.")
        else:
            messages.error(request, "Некорректно заполнена форма. Проверьте данные.")
    else:
        form = UserLoginForm()

    context = {
        'title': 'Вход в систему',
        'form': form
    }
    return render(request, 'accounts/accounts_form.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            messages.success(request, f"{user.username}, Вы успешно зарегистрировались.")
            return HttpResponseRedirect(reverse('blog:home'))
        else:
            messages.error(request, "Ошибка при регистрации. Проверьте введенные данные.")
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Регистрация',
        'form': form
    }
    return render(request, 'accounts/accounts_form.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('blog:home'))


@login_required
def profile(request):
    if request.method == 'POST':
        if 'delete_image' in request.POST:
            # Удаление изображения
            request.user.image.delete()
            request.user.save()
            return redirect('accounts:profile')
        else:
            # Сохранение изменений профиля
            form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
            if form.is_valid():
                form.save()
                return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})
