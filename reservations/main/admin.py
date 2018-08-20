from django.contrib import admin

from .models import Restaurant, Reservation, UserProfile

admin.site.register(Restaurant)
admin.site.register(Reservation)
admin.site.register(UserProfile)

