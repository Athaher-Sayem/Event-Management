from django.urls import path
from events.views import Home_view, Today_view, Upcomming_view, Past_view, About_view, Create_Event, Participant_Reg,Participant_List

urlpatterns = [
    path('Home/', Home_view, name='home'),
    path('Today_Events/', Today_view, name='today_events'),
    path('Upcomming_Events/', Upcomming_view, name='upcoming_events'),
    path('Past_Events/', Past_view, name='past_events'),
    path('About_Us/', About_view, name='about_us'),
    path('Create_Event/', Create_Event, name='Create_Event'),
    path('Participant_Reg/', Participant_Reg, name='Participant_Reg'),
    path('Participant/', Participant_List, name='Participant'),
]