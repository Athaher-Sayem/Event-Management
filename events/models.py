from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    cat_name  = models.CharField(max_length=50)
    cat_description  = models.TextField()

    def __str__(self):
        return self.cat_name

class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_description  = models.TextField()
    location = models.CharField(max_length=100)
    
    date_time = models.DateTimeField(default=timezone.now)

    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=1)

   
    image = models.ImageField(upload_to='event_images/', default='default_img.jpg')

    participants = models.ManyToManyField(User, related_name='events', blank=True)

    def __str__(self):
        return self.event_name
    

# class  Participant(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(blank=True)
    
#     def str(self): 
#         return self.user.get_username()

class RSPV(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvp_entries')
    user  = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='rsvp_entries')