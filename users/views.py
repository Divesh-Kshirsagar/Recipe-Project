from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


APP_NAME = 'users'

def login_page(request):
    if request.user.is_authenticated:  # Check if the user is logged in
        return redirect('/')  
    data = request.POST
    if request.method == "POST":
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(
            username = username,
            password = password
        )
        
        if user is None :
            messages.info(request, 'Invalid Credentials.')
            return render(request, 'users/login.html')
        else:
            login(request, user)
            return redirect('/')
    
    return render(request, 'users/login.html')


def register_page(request):
    if request.user.is_authenticated:  # Check if the user is logged in
        return redirect('/')  
    data = request.POST
    if request.method == "POST":
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        user_filter = User.objects.filter(
            username = username
        )
        
        if user_filter.exists():
            messages.info(request, 'Username already exist.')
            return render(request, 'users/register.html')
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email,
        )
        
        if password == confirm_password:
            user.set_password(password)
        
        user.save()
        
        messages.info(request, 'Account created successfully.')
        return redirect('Home:index')
    
    return render(request, 'users/register.html')


@login_required
def logout_page(request):
    logout(request)
    return redirect('users:login')