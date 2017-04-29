from django.db import models
from django.utils import timezone


class Reservations(models.Model):
    res_number = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 50)
    room = models.CharField(max_length = 50)
    date = models.DateField(max_length = 50, default=timezone.now)
    start_time = models.TimeField(default=timezone.now)
    reserved = models.BooleanField(default=False)

    def __str__(self):
        return "Reservation Number: " + str(self.res_number) + " Reserved Room: " + self.room + \
               ", Reserver Name: " + self.name + " Reservation Date: " + str(self.date) + \
               " Rseervation time: " + str(self.start_time) + " Reserved: " + str(self.reserved)

class Rooms(models.Model):
    room = models.CharField(max_length = 50,primary_key = True)
    category = models.CharField(max_length = 50)

    def __str__(self):
        return "Category: " + self.category + ", Room: " + self.room
