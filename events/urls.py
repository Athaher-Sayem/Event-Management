from django.urls import path
from events.views import *
from django.views.generic import RedirectView

urlpatterns = [
    path('', Home_view, name='home'),
    # path('Home/', Home_view, name='home'),
    path('Today_Events/', Today_view, name='today_events'),
    path('Upcomming_Events/', Upcomming_view, name='upcoming_events'),
    path('Past_Events/', Past_view, name='past_events'),
    path('About_Us/', About_view, name='about_us'),
    path('Create_Event/', Create_Event, name='Create_Event'),
    path('Participant_Reg/', Participant_Reg, name='Participant_Reg'),
    path('Participant/', Participant_List, name='Participant'),
    path('delete/<int:event_id>/',delete_event, name='delete_event'),
    path('Participant_Event/<int:event_id>/', event_participant_view, name='event_participant_view'),
    path('Update_View/<int:event_id>/', Update_view, name='update_view'),
    path('search/', Search_event_view, name='Search_event_view'),
]