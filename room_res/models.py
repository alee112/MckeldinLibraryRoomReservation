from django.db import models


# import datetime
# from django.utils import timezone

class Reservations(models.Model):
    res_number = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 50)
    room = models.CharField(max_length = 50)
    datetime = models.DateTimeField()
    reserved = models.BooleanField(default=False)
    


   


class Rooms(models.Model):
    room = models.CharField(max_length = 50,primary_key = True)
    category = models.CharField(max_length = 50)

    



    # class Room(models.Model):
    # 	Name = models.CharField(max_length=50)
    # 	def __str__(self):
    # 		return self.name

    # class RoomSystem(models.Model):
    # 	Time = models.CharField(max_length=50
    # 	def __str__(self):
    # 		return self.name