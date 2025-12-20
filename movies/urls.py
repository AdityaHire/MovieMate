from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.home, name='home'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('shows/', views.shows_list, name='shows_list'),
    path('about/', views.about, name='about'),
    
    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Booking URLs
    path('booking/<int:show_id>/', views.booking_page, name='booking'),
    path('payment/<int:booking_id>/', views.payment_page, name='payment'),
    path('booking/confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]
