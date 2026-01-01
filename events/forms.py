from django import forms
from events.models import Event

class Create_Task(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'event_description': forms.Textarea(attrs={'rows': 3}),
        }

       