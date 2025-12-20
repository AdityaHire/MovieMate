import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_booking.settings')
django.setup()

from movies.models import Movie, Theater, Show
from datetime import date, time, timedelta

# Create Theaters
theaters_data = [
    {'name': 'PVR Cinemas', 'location': 'Phoenix Mall, Mumbai', 'capacity': 200},
    {'name': 'INOX Multiplex', 'location': 'Select City Walk, Delhi', 'capacity': 180},
    {'name': 'Cinepolis', 'location': 'DLF Cyberhub, Gurgaon', 'capacity': 150},
    {'name': 'Miraj Cinema', 'location': 'R City Mall, Mumbai', 'capacity': 170},
    {'name': 'Carnival Cinemas', 'location': 'Phoenix Market City, Bangalore', 'capacity': 160},
]

print('Adding theaters...')
theaters = []
for theater_data in theaters_data:
    theater, created = Theater.objects.get_or_create(
        name=theater_data['name'],
        defaults={
            'location': theater_data['location'],
            'capacity': theater_data['capacity']
        }
    )
    theaters.append(theater)
    if created:
        print(f'  ✅ Created: {theater.name}')
    else:
        print(f'  ℹ️  Already exists: {theater.name}')

# Get all movies
movies = Movie.objects.all()
print(f'\nFound {movies.count()} movies in database')

# Create shows for upcoming dates
show_times = [
    time(10, 0),   # 10:00 AM
    time(13, 30),  # 1:30 PM
    time(17, 0),   # 5:00 PM
    time(20, 30),  # 8:30 PM
]

# Generate shows for next 7 days
today = date.today()
show_dates = [today + timedelta(days=i) for i in range(7)]

print('\nAdding shows...')
shows_created = 0
shows_existing = 0

for movie in movies:
    # Each movie gets shows at 2-3 random theaters
    import random
    selected_theaters = random.sample(theaters, min(3, len(theaters)))
    
    for theater in selected_theaters:
        # Each theater shows the movie 2-3 times per day for next 7 days
        selected_times = random.sample(show_times, random.randint(2, 3))
        
        for show_date in show_dates:
            for show_time in selected_times:
                show, created = Show.objects.get_or_create(
                    movie=movie,
                    theater=theater,
                    show_date=show_date,
                    show_time=show_time,
                    defaults={
                        'available_seats': theater.capacity,
                        'price': 250.00  # Base price
                    }
                )
                
                if created:
                    shows_created += 1
                else:
                    shows_existing += 1

print(f'  ✅ Created {shows_created} new shows')
print(f'  ℹ️  {shows_existing} shows already existed')

# Summary
print('\n' + '='*60)
print('📊 DATABASE SUMMARY')
print('='*60)
print(f'🎬 Movies: {Movie.objects.count()}')
print(f'🏢 Theaters: {Theater.objects.count()}')
print(f'🎫 Shows: {Show.objects.count()}')
print('='*60)

print('\n📋 Shows by Movie:')
for movie in movies[:10]:  # Show first 10 movies
    show_count = Show.objects.filter(movie=movie).count()
    print(f'  {movie.title}: {show_count} shows')

print('\n✅ All theaters and shows added successfully!')
print('🌐 Visit http://127.0.0.1:8000/ to see the updated listings!')
