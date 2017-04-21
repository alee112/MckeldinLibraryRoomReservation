from django.shortcuts import render
from .models import Reservations

# Create your views here.
from django.http import HttpResponse
from django.template import Context
from django.views.decorators.csrf import csrf_exempt

count = 0

@csrf_exempt
def index(request):
    if request.method == "POST":

        #coun tneeds to be updated otherwise we cant insert anymore

        fname = request.POST["fname"]
        lname = request.POST["lname"]
        time = request.POST["time"]
        date = request.POST["date"]
        room = request.POST["room"]
        uid = request.POST["uid"]
        email = request.POST["email"]

        # TODO: Do the DB stuff
        # student = Student(UID=uid, first_name=fname, last_name=lname)
        # student.save()

        last_res = Reservations.objects.all().order_by("res_number").last()
        id = 0
        if last_res is not None:
            id = last_res.res_number + 1

        room = Reservations(res_number = id, name = fname + lname, room = room, date = date, start_time = time,
            end_time = time)
        room.save()

        # TODO: Send confirmation email

        # output = fname + " " + lname + " (UID:" + uid + "), you have tentatively booked " + room + \
        #          " for " + date + " at " + time + ". Please check your email to confirm the booking."

        output = "confirmed"
        context = Context({'output': output})
        return render(request, 'index.html', context)

    else:
        context = Context({'output': ""})
        return render(request, 'index.html', context)
