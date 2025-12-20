from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from django.db import transaction
from django import forms
from django.utils import timezone
from .models import Movie, Show, Theater, Booking
from datetime import date
import uuid


# Customize form field attributes
def customize_form(form):
    """Add Bootstrap classes to form fields"""
    for field_name, field in form.fields.items():
        field.widget.attrs['class'] = 'form-control'
        if isinstance(field.widget, forms.PasswordInput):
            field.widget.attrs['placeholder'] = 'Enter password'
        elif isinstance(field.widget, forms.TextInput):
            field.widget.attrs['placeholder'] = f'Enter {field.label.lower()}'

def home(request):
    """
    Dynamic home page displaying all active movies
    """
    # Get all active movies
    movies = Movie.objects.filter(is_active=True)
    
    # Get search query if exists
    search_query = request.GET.get('search', '')
    if search_query:
        movies = movies.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(genre__icontains=search_query)
        )
    
    # Get genre filter if exists
    genre_filter = request.GET.get('genre', '')
    if genre_filter:
        movies = movies.filter(genre=genre_filter)
    
    context = {
        'movies': movies,
        'search_query': search_query,
        'genre_filter': genre_filter,
        'genres': Movie.GENRE_CHOICES,
    }
    return render(request, 'movies/home.html', context)


def movie_detail(request, movie_id):
    """
    Movie detail page with available shows
    """
    movie = get_object_or_404(Movie, id=movie_id)
    # Show all shows for this movie (including past for demo)
    shows = Show.objects.filter(movie=movie).select_related('theater').order_by('show_date', 'show_time')
    
    # If you want only upcoming shows, uncomment the line below:
    # shows = shows.filter(show_date__gte=date.today())
    
    context = {
        'movie': movie,
        'shows': shows,
    }
    return render(request, 'movies/movie_detail.html', context)


def shows_list(request):
    """
    List all upcoming shows
    """
    # Get all shows, not just future ones (for testing/demo purposes)
    shows = Show.objects.all().select_related('movie', 'theater').order_by('show_date', 'show_time')
    
    # If you want to filter by upcoming only, uncomment the line below:
    # shows = shows.filter(show_date__gte=date.today())
    
    context = {
        'shows': shows,
        'total_shows': shows.count(),
    }
    return render(request, 'movies/shows_list.html', context)


def about(request):
    """
    About page with team information
    """
    return render(request, 'movies/about.html')


def register_view(request):
    """
    User registration page
    """
    if request.user.is_authenticated:
        return redirect('movies:home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('movies:home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    customize_form(form)
    return render(request, 'movies/register.html', {'form': form})


def login_view(request):
    """
    User login page
    """
    if request.user.is_authenticated:
        return redirect('movies:home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next', 'movies:home')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    customize_form(form)
    return render(request, 'movies/login.html', {'form': form})


def logout_view(request):
    """
    User logout
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('movies:home')


@login_required
def booking_page(request, show_id):
    """
    Booking page with seat selection
    """
    show = get_object_or_404(Show, id=show_id)
    
    if request.method == 'POST':
        seats_requested = int(request.POST.get('seats', 0))
        
        if seats_requested <= 0:
            messages.error(request, 'Please select at least one seat.')
        elif seats_requested > show.available_seats:
            messages.error(request, f'Only {show.available_seats} seats available.')
        else:
            total_price = seats_requested * show.price
            
            # Create booking with transaction to prevent race conditions
            try:
                with transaction.atomic():
                    # Refresh show data to get latest seat availability
                    show = Show.objects.select_for_update().get(id=show_id)
                    
                    # Double-check availability after locking
                    if seats_requested > show.available_seats:
                        messages.error(request, f'Sorry! Only {show.available_seats} seats available now. Another user may have just booked.')
                        return redirect('movies:booking', show_id=show_id)
                    
                    # Create the booking with pending payment
                    booking = Booking.objects.create(
                        user=request.user,
                        show=show,
                        seats_booked=seats_requested,
                        total_price=total_price,
                        payment_status='PENDING'
                    )
                    
                    # Update available seats
                    show.available_seats -= seats_requested
                    show.save()
                
                # Redirect to payment page
                return redirect('movies:payment', booking_id=booking.id)
            except Exception as e:
                messages.error(request, 'An error occurred while processing your booking. Please try again.')
                return redirect('movies:booking', show_id=show_id)
    
    context = {
        'show': show,
    }
    return render(request, 'movies/booking.html', context)


@login_required
def payment_page(request, booking_id):
    """
    Payment page for booking
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Redirect if already paid
    if booking.payment_status == 'COMPLETED':
        return redirect('movies:booking_confirmation', booking_id=booking.id)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        if not payment_method:
            messages.error(request, 'Please select a payment method.')
        else:
            # Validate payment details based on method
            validation_errors = []
            
            if payment_method in ['CREDIT_CARD', 'DEBIT_CARD']:
                card_number = request.POST.get('card_number', '').replace(' ', '')
                card_holder = request.POST.get('card_holder', '')
                expiry_date = request.POST.get('expiry_date', '')
                cvv = request.POST.get('cvv', '')
                
                if not card_number or len(card_number) != 16 or not card_number.isdigit():
                    validation_errors.append('Invalid card number. Must be 16 digits.')
                if not card_holder or len(card_holder) < 3:
                    validation_errors.append('Please enter card holder name.')
                if not expiry_date or len(expiry_date) != 5:
                    validation_errors.append('Invalid expiry date. Format: MM/YY')
                if not cvv or len(cvv) != 3 or not cvv.isdigit():
                    validation_errors.append('Invalid CVV. Must be 3 digits.')
                    
            elif payment_method == 'UPI':
                upi_id = request.POST.get('upi_id', '')
                if not upi_id or '@' not in upi_id:
                    validation_errors.append('Invalid UPI ID. Format: username@bank')
                    
            elif payment_method == 'NET_BANKING':
                bank_name = request.POST.get('bank_name', '')
                if not bank_name:
                    validation_errors.append('Please select a bank.')
                    
            elif payment_method == 'WALLET':
                wallet_type = request.POST.get('wallet_type', '')
                if not wallet_type:
                    validation_errors.append('Please select a wallet.')
            
            if validation_errors:
                for error in validation_errors:
                    messages.error(request, error)
            else:
                try:
                    with transaction.atomic():
                        # Simulate payment processing
                        booking = Booking.objects.select_for_update().get(id=booking_id)
                        
                        # Generate payment ID
                        payment_id = f"PAY{uuid.uuid4().hex[:12].upper()}"
                        
                        # Simulate 10% chance of payment failure for realism
                        import random
                        if random.random() < 0.1:  # 10% failure rate
                            booking.payment_status = 'FAILED'
                            booking.save()
                            messages.error(request, '❌ Payment failed. Please check your payment details and try again.')
                            return redirect('movies:payment', booking_id=booking_id)
                        
                        # Update booking with payment info
                        booking.payment_status = 'COMPLETED'
                        booking.payment_method = payment_method
                        booking.payment_id = payment_id
                        booking.payment_date = timezone.now()
                        booking.save()
                    
                    messages.success(request, f'✅ Payment successful! Transaction ID: {payment_id}')
                    return redirect('movies:booking_confirmation', booking_id=booking.id)
                except Exception as e:
                    messages.error(request, '❌ Payment processing error. Please try again.')
                    return redirect('movies:payment', booking_id=booking_id)
    
    context = {
        'booking': booking,
        'payment_methods': Booking.PAYMENT_METHOD_CHOICES,
    }
    return render(request, 'movies/payment.html', context)


@login_required
def booking_confirmation(request, booking_id):
    """
    Booking confirmation page
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Redirect to payment if not paid
    if booking.payment_status != 'COMPLETED':
        messages.warning(request, 'Please complete payment to confirm your booking.')
        return redirect('movies:payment', booking_id=booking.id)
    
    context = {
        'booking': booking,
    }
    return render(request, 'movies/booking_confirmation.html', context)


@login_required
def my_bookings(request):
    """
    User's booking history
    """
    bookings = Booking.objects.filter(user=request.user).select_related(
        'show__movie', 'show__theater'
    ).order_by('-booking_date')
    
    context = {
        'bookings': bookings,
    }
    return render(request, 'movies/my_bookings.html', context)
