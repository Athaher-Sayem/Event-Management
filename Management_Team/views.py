from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, LoginForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

User = get_user_model()


def SignUpView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Set user as inactive until email activation
            user.is_active = False
            user.save()
            
            # Assign user to Participant group by default
            try:
                participant_group = Group.objects.get(name='Participant')
                user.groups.add(participant_group)
            except Group.DoesNotExist:
                # If group doesn't exist, create it
                participant_group = Group.objects.create(name='Participant')
                user.groups.add(participant_group)
            
            messages.success(request, 'Registration successful! Please check your email to activate your account.')
            return redirect('login')
    else:
        form = SignUpForm()

    return render(request, 'Dashboard/sign_up.html', {'form': form})


def LogInView(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            # Check if user account is activated
            if not user.is_active:
                messages.error(request, 'Your account is not activated. Please check your email for the activation link.')
                return redirect('login')
            
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            
            # Redirect to appropriate dashboard based on role
            if user.groups.filter(name='Admin').exists():
                return redirect('admin_dashboard')
            elif user.groups.filter(name='Organizer').exists():
                return redirect('organizer_dashboard')
            else:
                return redirect('participant_dashboard')
    else:
        form = LoginForm()

    return render(request, 'Dashboard/login.html', {'form': form})


def LogOutView(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully! You can now login.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link. Please contact support.')
        return redirect('home')
