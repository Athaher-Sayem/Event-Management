from django.shortcuts import render,redirect
from .forms import SignUpForm,LoginForm
from django.contrib.auth import login, logout
# Create your views here.

def SignUpView(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form=SignUpForm()

    return render(request,'Dashboard/Sign_Up.html',{'form':form})


def LogInView(request):
     if request.method =='POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    
     else:
       form=LoginForm()

     return render(request,'Dashboard/login.html',{'form':form})
