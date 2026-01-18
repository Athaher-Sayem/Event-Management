from django.urls import path
from .views import SignUpView,LogInView

urlpatterns = [
    path('sign-up/',SignUpView,name='sign-up'),
    path('login/',LogInView,name='login')
]
