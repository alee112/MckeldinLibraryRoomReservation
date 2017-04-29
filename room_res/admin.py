from django.contrib import admin
from .models import Reservations
from .models import Rooms
from .forms import ResSlotsForm
from datetime import *

class reservation_admin(admin.ModelAdmin):
    form = ResSlotsForm

    def save_model(self, request, obj, form, change):

        # Get data from form
        all = form.cleaned_data['all_in_category']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        duration = form.cleaned_data['duration']

        # Get the number of time slots per day and number of days
        slots_per_day = (datetime.combine(date.today(), end_time) -
                         datetime.combine(date.today(), start_time)).total_seconds() / 60 / duration
        num_days = (end_date - start_date).days + 1

        # Get the rooms
        rooms = []
        if all:
            category = form.cleaned_data['room_category'].category
            room_objs = Rooms.objects.filter(category=category)
            for x in room_objs:
                rooms.append(x.room)
        else:
            rooms.append(form.cleaned_data['room_category'].room)

        # Get the next reservation id
        id = 0
        last_res = Reservations.objects.all().order_by("res_number").last()
        if last_res is not None:
            id = last_res.res_number + 1

        # Add all of the time slots to all of the rooms
        for room in rooms:
            for day in range(num_days):
                for slot in range(int(slots_per_day)):
                    res_date = start_date + timedelta(days=day + 1)
                    start_time_datetime = datetime.combine(res_date, start_time) + timedelta(minutes=duration * slot)
                    obj.res_number=id
                    obj.room=room
                    obj.date=res_date
                    obj.start_time=start_time_datetime
                    super(reservation_admin, self).save_model(reservation_admin, obj=obj, form=form, change=change)
                    id += 1

admin.site.register(Reservations, reservation_admin)
admin.site.register(Rooms)

