from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def login_user(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username,password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            context['errors'] = 'Username or Password wrong!!!'
            context['username'] = username
            context['password'] = password
    return render(request, 'authen/login.html', context=context)

def logout_user(request):
    logout(request)
    return redirect('login')