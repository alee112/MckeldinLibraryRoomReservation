from django import forms
from functools import partial
from .models import Reservations, Rooms

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())

class ResSlotsForm(forms.ModelForm):
    # Get and set categories
    res_categories = Rooms.objects.all().order_by('category')
    room_category = forms.ModelChoiceField(res_categories, label="Rooms and Categories",
                                           help_text="Choose the category of rooms you want to add"
                                                                     "available reservations slots to.")

    # Other entries
    all_in_category = forms.BooleanField(help_text="Check this box if you want to apply these reservation time slots to"
                                                   "all rooms in the category of the selected room.", required=False)
    duration = forms.IntegerField(label="Duration of Reservations", help_text="Set the duration in minutes of each reservation time slot.")
    start_time = forms.TimeField(help_text="Set the first available time during the day that a reservation can be made")
    end_time = forms.TimeField(help_text="Set the time the last reservation time slot of the day should end.")
    start_date = forms.DateField(help_text="Set the reservation time slots to be available beginning on this day.")
    end_date = forms.DateField(help_text="Set this day to be the last day that the reservation time slots are available.")

    class Meta:
        model = Reservations
        fields = []