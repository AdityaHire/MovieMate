from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Movie(models.Model):
    GENRE_CHOICES = [
        ('ACTION', 'Action'),
        ('COMEDY', 'Comedy'),
        ('DRAMA', 'Drama'),
        ('HORROR', 'Horror'),
        ('ROMANCE', 'Romance'),
        ('THRILLER', 'Thriller'),
        ('SCI-FI', 'Science Fiction'),
        ('ANIMATION', 'Animation'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    duration = models.IntegerField(help_text="Duration in minutes")
    release_date = models.DateField()
    poster = models.ImageField(upload_to='movie_posters/', blank=True, null=True)
    trailer_url = models.URLField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(0)], default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-release_date']
    
    def __str__(self):
        return self.title


class Theater(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    capacity = models.IntegerField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.location}"


class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='shows')
    show_date = models.DateField()
    show_time = models.TimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available_seats = models.IntegerField()
    
    class Meta:
        ordering = ['show_date', 'show_time']
        unique_together = ['movie', 'theater', 'show_date', 'show_time']
    
    def __str__(self):
        return f"{self.movie.title} - {self.theater.name} - {self.show_date} {self.show_time}"


class Booking(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('CREDIT_CARD', 'Credit Card'),
        ('DEBIT_CARD', 'Debit Card'),
        ('UPI', 'UPI'),
        ('NET_BANKING', 'Net Banking'),
        ('WALLET', 'Wallet'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='bookings')
    seats_booked = models.IntegerField(validators=[MinValueValidator(1)])
    booking_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment fields
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-booking_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.show.movie.title} - {self.seats_booked} seats"
