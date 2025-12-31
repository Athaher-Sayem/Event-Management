from django.urls import path
from events.views import Home_view,Today_view,Upcomming_view,Past_view,About_view

urlpatterns = [
    path('Home/', Home_view),
    path('Today_Events/', Today_view),
    path('Upcomming_Events/',Upcomming_view),
    path('Past_Events/',Past_view),
    path('About_Us/',About_view),
   
]