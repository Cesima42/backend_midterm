from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth import login
from .forms import UserRegistrationForm, LoginForm


def login_page(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.data.get('username'), password=form.data.get('password'))
            login(request, user)
            if user is not None:
                return redirect('/')
            else:
                form.add_error(field='username', error='Invalid password or login')
                return render(request, 'user/login.html', {'form': form})
        else:
            return render(request, 'user/login.html', {'form': form})


def register_page(request):
    if request.method == 'GET':
        form = UserRegistrationForm()
        return render(request, 'user/register.html', {'form': form})
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            auth_data = auth.authenticate(request, email=user.email, password=form.data.get('password'))
            if auth_data is not None:
                login(request, auth_data)
                return redirect('/')
            return redirect('/auth/login/')
        else:
            return render(request, 'user/register.html', {'form': form})


def logout_page(request):
    auth.logout(request)
    return redirect('/auth/login')
