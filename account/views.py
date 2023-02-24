from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import get_user_model


def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            User = get_user_model()
            try:
                User.objects.get(username=request.POST['username'])
                return render(request, 'account/signup.html', context={'error': 'Username already exists.'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password1'])
                user.save()
                print(user.password)
                auth.login(request, user)
                return redirect('hunt:homepage')
        else:
            return render(request, 'account/signup.html', context={'error': 'Passwords don\'t match'})
    return render(request, 'account/signup.html')


def login(request):
    if request.method == 'POST':
        username_or_email = request.POST['username_or_email']
        password = request.POST['password']
        User = get_user_model()
        if '@' in username_or_email:
            try:
                username_or_email = User.objects.get(email=username_or_email).username
            except User.DoesNotExist:
                username_or_email = ''
        user = auth.authenticate(username=username_or_email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('hunt:homepage')
        return render(request, 'account/login.html', context={'error': 'Your authentication data is not correct.'})
    return render(request, 'account/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('hunt:homepage')