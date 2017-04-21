from .models import Rooms
from django.contrib.staticfiles.finders import find

def onstart():
    f = open(find('roomlist.txt'),'r') 

    roomlist = {}


    current_val = ""


    for line in f:
        if(':' in line):
            current_val = line.strip('\n').strip(':')
        elif(line != '\n'):
            roomlist[line.strip('\n')] = current_val

    for key in roomlist:
	    room = Rooms(room = key,category = roomlist[key])
	    room.save()
    print('Insert Successful!')




        
