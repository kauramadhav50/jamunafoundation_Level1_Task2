from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages as message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


def home(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == "POST":
        data = request.POST
        email = data.get('email')
        password = data.get('password')

        # Check if user with email exists
        if not User.objects.filter(email=email).exists():
            message.error(request, 'Email is not registered')
            return redirect('login')

        # Get the username from email
        username = User.objects.get(email=email).username

        # Authenticate using username and password
        user = authenticate(username=username, password=password)

        if user is None:
            message.error(request, 'Invalid password')
            return redirect('login')
        else:
            login(request, user)
            message.success(request, f'Welcome back, {user.username}!')
            return redirect('home')

    return render(request, 'login_page.html')

@login_required(login_url='login')
def donation(request):
    return render(request, 'donation.html')
    

def register(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('name')
        email = data.get('email')
        password = data.get('password')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            message.info(request, 'Email already registered')
            return redirect('register')

        # Create user properly
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()

        message.success(request, 'Registration successful! Please log in.')
        return redirect('login')

    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    message.success(request, 'You have been logged out.')
    return redirect('home')


@login_required(login_url='login')
def dashboard(request):
    user = User.objects.get(id=request.user.id)
    
    return render(request, 'dashboard.html', {'user': user})

@login_required(login_url='login')
def profile(request):
    user = request.user

    if request.method == "POST":
        # Handle profile update logic here
        current_password = request.POST.get('current-password')
        new_password = request.POST.get('new-password')

        if current_password and new_password:
            # Authenticate user with their current password
            auth_user = authenticate(username=user.username, password=current_password)
            if auth_user:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # ✅ Keeps user logged in
                message.success(request, "Password changed successfully!")  # ✅ fixed “message” → “messages”
            else:
                message.error(request, "Current password is incorrect.")

        return redirect('home')

    return render(request, 'profile.html')