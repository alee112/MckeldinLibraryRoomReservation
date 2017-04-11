from django.shortcuts import render
from .models import Student

# Create your views here.
from django.http import HttpResponse
from django.template import Context
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        time = request.POST["time"]
        date = request.POST["date"]
        room = request.POST["room"]
        uid = request.POST["uid"]
        email = request.POST["email"]

        # TODO: Do the DB stuff
        student = Student(UID=uid, first_name=fname, last_name=lname)
        student.save()

        # TODO: Send confirmation email

        output = fname + " " + lname + " (UID:" + uid + "), you have tentatively booked " + room + \
                 " for " + date + " at " + time + ". Please check your email to confirm the booking."
        context = Context({'output': output})
        return render(request, 'index.html', context)

    else:
        context = Context({'output': ""})
        return render(request, 'index.html', context)
