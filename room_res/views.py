from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import Context
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    if request.method == "POST":
        name = request.POST["Name"]
        time = request.POST["Time"]
        context = Context({'name':name}, {'time':time})
        return render(request, 'index.html', context)

    else:
        context = Context({'name':""}, {'time':""})
        return render(request, 'index.html', context)

def test(request):
	context = Context({'some_num': 134 })
	return render(request, 'dummy.html', context)

#Working on getting field values from html
#def field_values(request):
#    room = request.GET[Room Id']
#        if room.is_valid():
#            room_id = room.cleaned_data['value']
#    time = request.GET['time']
#        if time.is_valid():
#            time_value = time.cleaned_data['value']
#    name = request.GET['name']
#        if name.is_valid():
#            name_value = room.cleaned_data['value']
