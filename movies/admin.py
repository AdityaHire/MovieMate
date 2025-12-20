from django.contrib import admin
from .models import Movie, Theater, Show, Booking

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'duration', 'release_date', 'is_active']
    list_filter = ['genre', 'is_active', 'release_date']
    search_fields = ['title', 'description']

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'capacity']
    search_fields = ['name', 'location']

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ['movie', 'theater', 'show_date', 'show_time', 'price', 'available_seats']
    list_filter = ['show_date', 'theater']
    search_fields = ['movie__title', 'theater__name']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'show', 'seats_booked', 'booking_date', 'total_price', 'payment_status', 'payment_method']
    list_filter = ['booking_date', 'payment_status', 'payment_method']
    search_fields = ['user__username', 'show__movie__title', 'payment_id']
