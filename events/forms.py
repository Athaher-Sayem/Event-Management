from django import forms
from .models import Event

from django import forms
from events.models import Event

class Create_Task(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

        style = "w-full bg-white border border-gray-300 text-gray-700 py-3 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-200"

        widgets = {
            'event_name': forms.TextInput(attrs={'class': style, 'placeholder': 'Enter event name'}),
            'event_description': forms.Textarea(attrs={'class': style, 'rows': 4, 'placeholder': 'Describe the details...'}),
            'location': forms.TextInput(attrs={'class': style, 'placeholder': 'Where is it happening?'}),
            'date_time': forms.DateTimeInput(attrs={'class': style, 'type': 'datetime-local'}),
            'category': forms.Select(attrs={'class': style}),
        }