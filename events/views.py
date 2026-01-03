from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Participant
from .forms import Create_Task
from django.utils import timezone
from django.contrib import messages
from django.db.models import Count, Q 

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
    parti = Participant.objects.all()
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

    context = {
        'events': all_events,          
        'total_count': counts['total'],    
        'upcoming_count': counts['upcoming'],
        'past_count': counts['past'],
        'today_count': counts['today'],
    }
    
    return render(request, "Home.html", context)


def Today_view(request):
    now = timezone.now()
    today_events = Event.objects.select_related('category').filter(date_time__date=now.date())
    patcount = Participant.objects.filter(events__in=today_events).distinct().count()
    
    context = {
        'patcount': patcount,
        'events': today_events,          
        'today_count': today_events.count(),
    }
    
    return render(request, "Today.html", context)


def Upcomming_view(request):
    now = timezone.now()
    upcoming_events = Event.objects.select_related('category').filter(date_time__gt=now)
    
    patcount = Participant.objects.filter(events__in=upcoming_events).distinct().count()
    
    context = {
        'patcount': patcount,
        'events': upcoming_events,          
        'upcomming_count': upcoming_events.count(),
    }
    
    return render(request, "Upcomming.html", context)


def Past_view(request):
    now = timezone.now()
    past_events = Event.objects.select_related('category').filter(date_time__lt=now)
    
    patcount = Participant.objects.filter(events__in=past_events).distinct().count()
    
    context = {
        'patcount': patcount,
        'events': past_events,          
        'past_count': past_events.count(),
    }
    return render(request, "Past.html", context)


def About_view(request):
    return render(request, "About.html")


def Participant_List(request):
    participants = Participant.objects.prefetch_related('events').all()
    
    total_participants = participants.count() 
    context = {
        'participants': participants,
        'total_participants': total_participants,
    }
    
    return render(request, "Participant_List.html", context)


def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id) 
    event_name = event.event_name
    event.delete()
    
    messages.success(request, f"'{event_name}' Event Deleted")
    return redirect('home') 

def event_participant_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participants = Participant.objects.filter(events=event)
    total = participants.count()

    return render(request, "Participant_Event.html", {
        'event': event,
        'participants': participants,
        'total_participants': total
    })

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