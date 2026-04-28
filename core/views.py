from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from .forms import LoginForm

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                auth_login(request, user)
                next_url = request.GET.get('next') or request.POST.get('next') or 'questions:index'
                if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                return redirect('questions:index')
            else:
                form.add_error(None, "Неверный логин или пароль") 
    else:
        form = LoginForm()

    return render(request, 'core/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect(request.META.get('HTTP_REFERER', 'questions:index'))

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user) 
            return redirect('questions:index')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})