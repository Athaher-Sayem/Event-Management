from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Category
from .forms import Create_Task
from django.utils import timezone
from django.contrib import messages
from django.db.models import Count, Q 
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import organizer_required, admin_required, role_required
User = get_user_model()

@organizer_required
def Create_Event(request):
    if request.method == 'POST':
        form = Create_Task(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:
        form = Create_Task()

    return render(request, "Create_Event.html", {'form': form})

def Participant_Reg(request):
    parti = User.objects.all()
    return render(request, "Participant.html", {'Parti': parti})


def Home_view(request):
    now = timezone.now()
    all_events = Event.objects.select_related('category').all().order_by('-date_time')
    counts = Event.objects.aggregate(
        total=Count('id'),
        upcoming=Count('id', filter=Q(date_time__gt=now)),
        past=Count('id', filter=Q(date_time__lt=now)),
        today=Count('id', filter=Q(date_time__date=now.date()))
    )

    # Check RSVP status for authenticated users
    user_rsvp_events = set()
    is_participant = False
    is_organizer = False
    is_admin = False
    
    if request.user.is_authenticated:
        user_rsvp_events = set(Event.objects.filter(participants=request.user).values_list('id', flat=True))
        user_groups = request.user.groups.values_list('name', flat=True)
        is_participant = 'Participant' in user_groups and 'Admin' not in user_groups and 'Organizer' not in user_groups
        is_organizer = 'Organizer' in user_groups
        is_admin = 'Admin' in user_groups

    context = {
        'events': all_events,          
        'total_count': counts['total'],    
        'upcoming_count': counts['upcoming'],
        'past_count': counts['past'],
        'today_count': counts['today'],
        'user_rsvp_events': user_rsvp_events,
        'is_participant': is_participant,
        'is_organizer': is_organizer,
        'is_admin': is_admin,
    }
    
    return render(request, "Home.html", context)


def Today_view(request):
    now = timezone.now()
    today_events = Event.objects.select_related('category').filter(date_time__date=now.date())
    patcount = User.objects.filter(events__in=today_events).distinct().count()
    
    context = {
        'patcount': patcount,
        'events': today_events,          
        'today_count': today_events.count(),
    }
    
    return render(request, "Today.html", context)


def Upcomming_view(request):
    now = timezone.now()
    upcoming_events = Event.objects.select_related('category').filter(date_time__gt=now)
    
    patcount = User.objects.filter(events__in=upcoming_events).distinct().count()
    
    context = {
        'patcount': patcount,
        'events': upcoming_events,          
        'upcomming_count': upcoming_events.count(),
    }
    
    return render(request, "Upcomming.html", context)


def Past_view(request):
    now = timezone.now()
    past_events = Event.objects.select_related('category').filter(date_time__lt=now)
    
    patcount = User.objects.filter(events__in=past_events).distinct().count()
    
    context = {
        'patcount': patcount,
        'events': past_events,          
        'past_count': past_events.count(),
    }
    return render(request, "Past.html", context)


def About_view(request):
    return render(request, "About.html")


@admin_required
def Participant_List(request):
    participants = User.objects.prefetch_related('events').all()
    
    total_participants = participants.count() 
    context = {
        'participants': participants,
        'total_participants': total_participants,
    }
    
    return render(request, "Participant_List.html", context)


@organizer_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id) 
    event_name = event.event_name
    event.delete()
    
    messages.success(request, f"'{event_name}' Event Deleted")
    return redirect('home') 

def event_participant_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participants = User.objects.filter(events=event)
    total = participants.count()

    return render(request, "Participant_Event.html", {
        'event': event,
        'participants': participants,
        'total_participants': total
    })

@organizer_required
def Update_view(request, event_id):
    single_event = get_object_or_404(Event, id=event_id)
    form = Create_Task(instance=single_event)

    if request.method == "POST":
        form = Create_Task(request.POST, instance=single_event)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Event Updated Successfully")
            return redirect('home') 
        
    return render(request, "Update_Event.html", {'form': form})

def Search_event_view(request):
    query = request.GET.get('q', '') 

    if query:
        results = Event.objects.select_related('category').filter(event_name__icontains=query)
    else:
        results = Event.objects.none()

    context = {
        'events': results,
        'query': query
    }

    return render(request, "Search.html", context)


# RSVP Views
@login_required
def rsvp_event(request, event_id):
    """Allow participants to RSVP to an event"""
    event = get_object_or_404(Event, id=event_id)
    
    # Check if user already RSVP'd
    if event.participants.filter(id=request.user.id).exists():
        messages.warning(request, f'You have already RSVP\'d to "{event.event_name}"')
        return redirect('home')
    
    # Add user to event participants (RSVP)
    event.participants.add(request.user)
    messages.success(request, f'Successfully RSVP\'d to "{event.event_name}"! Check your email for confirmation.')
    return redirect('home')


@login_required
def cancel_rsvp(request, event_id):
    """Allow participants to cancel their RSVP"""
    event = get_object_or_404(Event, id=event_id)
    
    if event.participants.filter(id=request.user.id).exists():
        event.participants.remove(request.user)
        messages.success(request, f'RSVP cancelled for "{event.event_name}"')
    else:
        messages.warning(request, 'You have not RSVP\'d to this event')
    
    return redirect('home')


# Dashboard Views
@admin_required
def admin_dashboard(request):
    """Admin Dashboard - Full access"""
    now = timezone.now()
    all_events = Event.objects.select_related('category').all().order_by('-date_time')
    all_participants = User.objects.all()
    all_categories = Category.objects.all()
    
    counts = Event.objects.aggregate(
        total=Count('id'),
        upcoming=Count('id', filter=Q(date_time__gt=now)),
        past=Count('id', filter=Q(date_time__lt=now)),
        today=Count('id', filter=Q(date_time__date=now.date()))
    )
    
    context = {
        'events': all_events,
        'participants': all_participants,
        'categories': all_categories,
        'total_events': counts['total'],
        'upcoming_events': counts['upcoming'],
        'past_events': counts['past'],
        'today_events': counts['today'],
        'total_participants': all_participants.count(),
        'total_categories': all_categories.count(),
    }
    
    return render(request, 'Dashboard/admin_dashboard.html', context)


@organizer_required
def organizer_dashboard(request):
    """Organizer Dashboard - Manage events and categories"""
    now = timezone.now()
    all_events = Event.objects.select_related('category').all().order_by('-date_time')
    all_categories = Category.objects.all()
    
    counts = Event.objects.aggregate(
        total=Count('id'),
        upcoming=Count('id', filter=Q(date_time__gt=now)),
        past=Count('id', filter=Q(date_time__lt=now)),
        today=Count('id', filter=Q(date_time__date=now.date()))
    )
    
    context = {
        'events': all_events,
        'categories': all_categories,
        'total_events': counts['total'],
        'upcoming_events': counts['upcoming'],
        'past_events': counts['past'],
        'today_events': counts['today'],
        'total_categories': all_categories.count(),
    }
    
    return render(request, 'Dashboard/organizer_dashboard.html', context)


@login_required
def participant_dashboard(request):
    """Participant Dashboard - View RSVP'd events"""
    user = request.user
    rsvp_events = Event.objects.filter(participants=user).select_related('category').order_by('-date_time')
    now = timezone.now()
    
    upcoming_rsvp = rsvp_events.filter(date_time__gt=now)
    past_rsvp = rsvp_events.filter(date_time__lt=now)
    today_rsvp = rsvp_events.filter(date_time__date=now.date())
    
    context = {
        'rsvp_events': rsvp_events,
        'upcoming_rsvp': upcoming_rsvp,
        'past_rsvp': past_rsvp,
        'today_rsvp': today_rsvp,
        'total_rsvp': rsvp_events.count(),
    }
    
    return render(request, 'Dashboard/participant_dashboard.html', context)


@admin_required
def delete_participant(request, user_id):
    """Admin can delete participants"""
    participant = get_object_or_404(User, id=user_id)
    
    # Prevent admin from deleting themselves
    if participant == request.user:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('admin_dashboard')
    
    username = participant.username
    participant.delete()
    messages.success(request, f'Participant "{username}" has been deleted.')
    return redirect('admin_dashboard')


@admin_required
def manage_groups(request):
    """Admin can manage groups"""
    groups = Group.objects.all()
    return render(request, 'Dashboard/manage_groups.html', {'groups': groups})


@admin_required
def change_user_role(request, user_id):
    """Admin can change user roles"""
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        role = request.POST.get('role')
        # Remove user from all groups
        user.groups.clear()
        
        # Add to selected group
        if role:
            try:
                group = Group.objects.get(name=role)
                user.groups.add(group)
                messages.success(request, f'Role changed to {role} for {user.username}')
            except Group.DoesNotExist:
                messages.error(request, f'Group "{role}" does not exist')
        
        return redirect('admin_dashboard')
    
    groups = Group.objects.all()
    return render(request, 'Dashboard/change_role.html', {'user': user, 'groups': groups})
