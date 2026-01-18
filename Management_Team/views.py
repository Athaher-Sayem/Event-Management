from django.shortcuts import render,redirect
from .forms import SignUpForm

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