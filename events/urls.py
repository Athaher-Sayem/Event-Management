from django.urls import path
from events.views import Home_view,Today_view,Upcomming_view,Past_view,About_view,Create_Event,Participant_Reg

urlpatterns = [
    path('Home/', Home_view),
    path('Today_Events/', Today_view),
    path('Upcomming_Events/',Upcomming_view),
    path('Past_Events/',Past_view),
    path('About_Us/',About_view),
    path('Create_Event/',Create_Event, name='Create_Event'),
    path('Participant_Reg/',Participant_Reg, name='Participant_Reg'),
   
]