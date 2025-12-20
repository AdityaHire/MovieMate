import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_booking.settings')
django.setup()

from movies.models import Movie
from datetime import date

# Clear existing movies if needed (optional)
# Movie.objects.all().delete()

# Action Movies
Movie.objects.get_or_create(
    title='Pathaan',
    defaults={
        'description': 'A fearless RAW agent embarks on a high-stakes mission to stop a dangerous terrorist group threatening India\'s security.',
        'genre': 'ACTION',
        'duration': 146,
        'release_date': date(2023, 1, 25),
        'rating': 7.5
    }
)

Movie.objects.get_or_create(
    title='Jawan',
    defaults={
        'description': 'A jailer and his team embark on a mission to rectify societal issues by taking matters into their own hands.',
        'genre': 'ACTION',
        'duration': 169,
        'release_date': date(2023, 9, 7),
        'rating': 7.8
    }
)

# Comedy Movies
Movie.objects.get_or_create(
    title='Fukrey 3',
    defaults={
        'description': 'The Fukrey boys return with another hilarious adventure filled with comedy and chaos.',
        'genre': 'COMEDY',
        'duration': 147,
        'release_date': date(2023, 9, 28),
        'rating': 6.5
    }
)

Movie.objects.get_or_create(
    title='Dream Girl 2',
    defaults={
        'description': 'Karam returns with his voice magic, getting into hilarious situations while pretending to be Pooja.',
        'genre': 'COMEDY',
        'duration': 138,
        'release_date': date(2023, 8, 25),
        'rating': 6.8
    }
)

# Drama Movies
Movie.objects.get_or_create(
    title='12th Fail',
    defaults={
        'description': 'Based on the true story of IPS officer Manoj Kumar Sharma\'s journey from failing his 12th exam to becoming a top officer.',
        'genre': 'DRAMA',
        'duration': 147,
        'release_date': date(2023, 10, 27),
        'rating': 9.2
    }
)

Movie.objects.get_or_create(
    title='Rocky Aur Rani Kii Prem Kahaani',
    defaults={
        'description': 'A love story between two individuals from contrasting families who must navigate their cultural differences.',
        'genre': 'DRAMA',
        'duration': 168,
        'release_date': date(2023, 7, 28),
        'rating': 7.3
    }
)

# Romance Movies
Movie.objects.get_or_create(
    title='Tu Jhoothi Main Makkaar',
    defaults={
        'description': 'A modern romantic comedy about love, relationships, and the complexities of commitment.',
        'genre': 'ROMANCE',
        'duration': 164,
        'release_date': date(2023, 3, 8),
        'rating': 6.9
    }
)

Movie.objects.get_or_create(
    title='Satyaprem Ki Katha',
    defaults={
        'description': 'A heartwarming love story about second chances and healing emotional wounds.',
        'genre': 'ROMANCE',
        'duration': 146,
        'release_date': date(2023, 6, 29),
        'rating': 7.4
    }
)

# Thriller Movies
Movie.objects.get_or_create(
    title='Jailer',
    defaults={
        'description': 'A retired jailer must confront his past when his family is threatened by dangerous criminals.',
        'genre': 'THRILLER',
        'duration': 168,
        'release_date': date(2023, 8, 10),
        'rating': 7.9
    }
)

Movie.objects.get_or_create(
    title='Khufiya',
    defaults={
        'description': 'A spy thriller about a RAW operative tracking down a mole within the organization.',
        'genre': 'THRILLER',
        'duration': 157,
        'release_date': date(2023, 10, 5),
        'rating': 6.7
    }
)

# Horror Movies
Movie.objects.get_or_create(
    title='Bhediya',
    defaults={
        'description': 'A man transforms into a wolf every full moon and must deal with the terrifying consequences.',
        'genre': 'HORROR',
        'duration': 156,
        'release_date': date(2022, 11, 25),
        'rating': 6.7
    }
)

Movie.objects.get_or_create(
    title='Gaslight',
    defaults={
        'description': 'A psychological thriller about a daughter who returns home to find disturbing secrets.',
        'genre': 'HORROR',
        'duration': 111,
        'release_date': date(2023, 3, 31),
        'rating': 5.9
    }
)

# Sci-Fi Movies
Movie.objects.get_or_create(
    title='Krrish',
    defaults={
        'description': 'A young man with superpowers must save the world from a brilliant but evil scientist.',
        'genre': 'SCI-FI',
        'duration': 154,
        'release_date': date(2006, 6, 23),
        'rating': 6.4
    }
)

Movie.objects.get_or_create(
    title='Robot',
    defaults={
        'description': 'A scientist creates a highly advanced humanoid robot, but things go wrong when it develops emotions.',
        'genre': 'SCI-FI',
        'duration': 174,
        'release_date': date(2010, 10, 1),
        'rating': 7.1
    }
)

# Animation Movies
Movie.objects.get_or_create(
    title='Hanuman',
    defaults={
        'description': 'An animated retelling of the legendary Hindu deity Hanuman\'s adventures and heroic deeds.',
        'genre': 'ANIMATION',
        'duration': 96,
        'release_date': date(2005, 10, 21),
        'rating': 6.8
    }
)

Movie.objects.get_or_create(
    title='Chhota Bheem: Curse of Damyaan',
    defaults={
        'description': 'India\'s favorite animated hero Chhota Bheem embarks on an adventure to save his kingdom.',
        'genre': 'ANIMATION',
        'duration': 96,
        'release_date': date(2012, 5, 18),
        'rating': 5.4
    }
)

print('✅ Successfully added Bollywood movies across all genres!')
print(f'📊 Total movies in database: {Movie.objects.count()}')
print('\nMovies by genre:')
for genre_code, genre_name in Movie.GENRE_CHOICES:
    count = Movie.objects.filter(genre=genre_code).count()
    print(f'  {genre_name}: {count} movies')
