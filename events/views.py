
from django.shortcuts import render, redirect
from .models import Event,Participant
from .forms import Create_Task
from django.utils import timezone


def Create_Event(request):
    if request.method == 'POST':
        form = Create_Task(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Create_Event')
    else:
        form = Create_Task()

    return render(request, "Create_Event.html", {'form': form})

def Participant_Reg(request):
    parti=Participant.objects.all()

    return render(request,"Participant.html",{'Parti':parti})


def Home_view(request):
    now = timezone.now()
    all_events = Event.objects.all()
    total_count = all_events.count()
    upcoming_count = Event.objects.filter(date_time__gt=now).count()
    past_count = Event.objects.filter(date_time__lt=now).count()
    today_count = Event.objects.filter(date_time__date=now.date()).count()

    context = {
        'events': all_events,          
        'total_count': total_count,    
        'upcoming_count': upcoming_count,
        'past_count': past_count,
        'today_count': today_count,
    }
    
    return render(request, "Home.html", context)


def Today_view(request):
    now = timezone.now()
    today = Event.objects.filter(date_time__date=now.date())
    patcount = Participant.objects.filter(events__in=today).distinct().count()
    today_count =today.count()
    context = {
        'patcount':patcount,
        'events': today,          
        'today_count': today_count,
    }
    
    return render(request,"Today.html",context)



def Upcomming_view(request):
    now = timezone.now()
    upcomming = Event.objects.filter(date_time__gt=now.date())
    upcomming_count =upcomming.count()

    patcount = Participant.objects.filter(events__in=upcomming).distinct().count()
    context = {
        'patcount':patcount,
        'events': upcomming,          
        'upcomming_count': upcomming_count,
    }
    
    return render(request,"Upcomming.html",context)




def Past_view(request):
    now = timezone.now()
    past_events = Event.objects.filter(date_time__lt=now)
    past_count = Event.objects.filter(date_time__lt=now).count()

    patcount = Participant.objects.filter(events__in=past_events).distinct().count()
    context = {
        'patcount':patcount,
        'events': past_events,          
        'past_count': past_count,
       
    }
    return render(request,"Past.html",context)



def About_view(request):
    return render(request,"About.html")

