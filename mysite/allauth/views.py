from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_page(request):
    if request.user.is_authenticated:
        return redirect('posts:blog')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('posts:blog')
            else:
                messages.error(request, 'Неверная почта или пароль')
                return render(request, 'accounts/login.html')
        return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    return redirect('allauth:login page')


def register(request):
    if request.user.is_authenticated:
        return redirect('posts:blog')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
        context = {'form': form}
        return render(request, 'accounts/register.html', context)
