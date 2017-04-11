from django.db import models


# import datetime
# from django.utils import timezone

class Student(models.Model):
    UID = models.IntegerField(primary_key = True)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)

    def __str__(self):
        return self.first_name +','+ last_name


    # class Room(models.Model):
    # 	Name = models.CharField(max_length=50)
    # 	def __str__(self):
    # 		return self.name

    # class RoomSystem(models.Model):
    # 	Time = models.CharField(max_length=50
    # 	def __str__(self):
    # 		return self.name