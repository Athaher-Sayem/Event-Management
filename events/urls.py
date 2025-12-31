from django.urls import path
from events.views import Home_view

urlpatterns = [
    path('Home/', Home_view),
   
]