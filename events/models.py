from django.db import models


class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_description = models.TextField()
    location = models.CharField(max_length=100)
    date_time= models.DateTimeField()

    category=models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        default=1
    )

    def __str__(self):
        return self.event_name


class Participant(models.Model):
    parti_name = models.CharField(max_length=100)
    email= models.EmailField(unique=True)

    events = models.ManyToManyField(Event, related_name='participants')
    def __str__(self):
        return self.parti_name



class Category(models.Model):
    cat_name = models.CharField(max_length=100)
    cat_description =models.TextField()

    def __str__(self):
        return self.cat_name
