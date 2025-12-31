from django.shortcuts import render
from django.http import HttpResponse

def Home_view(request):
    return render(request,"Home.html")


