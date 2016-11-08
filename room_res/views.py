from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
	# context = context = { 'instructor_list': Instructor.objects.all() }
 #    return render(request, 'grading/index.html', context)
    return HttpResponse("Hello. This is just a test.")