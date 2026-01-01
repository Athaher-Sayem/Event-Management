
from django.shortcuts import render, redirect
from .models import Event
from .forms import Create_Task


def Create_Event(request):
    if request.method == 'POST':
        form = Create_Task(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Create_Event')
    else:
        form = Create_Task()

    return render(request, "Create_Event.html", {'form': form})




def Home_view(request):
    return render(request,"Home.html")


def Today_view(request):
    return render(request,"Today.html")



def Upcomming_view(request):
    return render(request,"Upcomming.html")




def Past_view(request):
    return render(request,"Past.html")



def About_view(request):
    return render(request,"About.html")

