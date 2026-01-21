from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import Group


def role_required(*allowed_roles):
   
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Please login to access this page.')
                return redirect('login')
            
            
            user_groups = request.user.groups.values_list('name', flat=True)
            if not any(role in user_groups for role in allowed_roles):
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('home')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def admin_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to access this page.')
            return redirect('login')
        
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'Only administrators can access this page.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def organizer_required(view_func):
    
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to access this page.')
            return redirect('login')
        
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'Admin' not in user_groups and 'Organizer' not in user_groups:
            messages.error(request, 'Only organizers can access this page.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def participant_required(view_func):
    
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to access this page.')
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    return wrapper
