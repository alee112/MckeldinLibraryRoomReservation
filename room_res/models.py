from django.db import models


# import datetime
# from django.utils import timezone

class Reservations(models.Model):
    res_number = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 50)
    room = models.CharField(max_length = 50)
    date = models.CharField(max_length = 50)
    start_time = models.CharField(max_length = 50)
    end_time = models.CharField(max_length = 50)


    def __str__(self):
        return res_number + ''

    # class Room(models.Model):
    # 	Name = models.CharField(max_length=50)
    # 	def __str__(self):
    # 		return self.name

    # class RoomSystem(models.Model):
    # 	Time = models.CharField(max_length=50
    # 	def __str__(self):
    # 		return self.name