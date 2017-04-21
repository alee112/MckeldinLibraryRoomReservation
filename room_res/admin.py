from django.contrib import admin

from .models import Reservations

from .models import Rooms

admin.site.register(Reservations)

admin.site.register(Rooms)

# Register your models here.
