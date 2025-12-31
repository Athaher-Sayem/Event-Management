from django.shortcuts import render
from django.http import HttpResponse

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