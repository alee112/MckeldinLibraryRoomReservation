from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import Context


def index(request):
    context = Context({ 'some_num': 134 })
    return render(request, 'dummy.html', context)

#Working on getting field values from html
#def field_values(request):
#    room_id = request.getvalue('Room Id')
#    time = request.getvalue('time')
#    name = request.getvalue('name')
