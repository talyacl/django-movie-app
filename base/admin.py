from django.contrib import admin

# Register your models here.

from .models import Movie, Watchlist

admin.site.register(Movie)
admin.site.register(Watchlist)