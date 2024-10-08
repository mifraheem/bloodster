
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import User
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password


from bloodster.email_functions import send_verification_email


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
            # Create user instance and save as inactive
            user = User(
                username=username,
                email=email,
                password=make_password(password),
                user_type=user_type,
                is_active=False  # Set user as inactive initially
            )
            user.save()

            # Send verification email
            try:
                send_verification_email(user.email, user.verification_uuid)
                messages.success(
                    request, 'Registration successful! Please check your email to verify your account.'
                )
                return redirect('register')
            except Exception as e:
                print(f'Exception found: {e}')
                user.delete()
                messages.error(
                    request, 'Error sending verification email. Please try again later.')
                return redirect('register')

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


@csrf_exempt
def verify_user(request, verification_uuid):
    user = get_object_or_404(User, verification_uuid=verification_uuid)
    verified = False

    if request.method == 'POST':
        password = request.POST.get('password')
        if password:
            if check_password(password, user.password):
                user.is_active = True
                user.save()
                verified = True
                messages.success(
                    request, "Your account has been successfully verified!")
                return redirect('login')
            else:
                messages.error(
                    request, "Incorrect password. Please try again.")

    return render(request, 'web/verify.html', {'verified': verified, 'user': user})
