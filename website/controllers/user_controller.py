
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import User
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        user_type = request.POST.get('user_type')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')

        try:
            user = User(
                username=username,
                email=email,
                password=make_password(password),
                user_type=user_type
            )
            user.save()

            messages.success(
                request, 'Registration successful! You can now log in.')
            return redirect('login')
        except ValidationError as e:
            messages.error(request, f'Error: {e}')
            return redirect('register')

    return render(request, 'web/register.html')


@csrf_exempt
def handle_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Please provide both email and password.')
            return render(request, 'web/login.html')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'web/login.html')

        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'web/login.html')


def handle_logout(request):
    logout(request=request)
    messages.info(request, "You're Logged Out")
    return redirect('home')


@login_required
def update_profile(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        blood_group = request.POST.get('blood_group')
        location = request.POST.get('location')
        profile_picture = request.FILES.get('profile')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email address.")
            return redirect('update_profile')

        if User.objects.exclude(pk=user.pk).filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('update_profile')

        if User.objects.exclude(pk=user.pk).filter(email=email).exists():
            messages.error(request, "Email already taken.")
            return redirect('update_profile')

        user.username = username
        user.email = email
        user.phone_number = phone_number
        user.blood_group = blood_group
        user.location = location
        if profile_picture:
            user.profile = profile_picture

        user.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('update_profile')

    return render(request, 'web/profile.html')
