# MovieMate - Movie Booking Portal

A dynamic movie booking portal built with Django, HTML, CSS, and Bootstrap.

## ✨ Features

- 🎬 Browse movies with search and genre filters
- 🎫 View show schedules with theater information
- 💺 Book seats with real-time availability
- 💳 Payment processing
- 📋 Booking history and confirmation
- 👤 User authentication (register/login)
- 📊 Admin panel for managing movies, theaters, shows, and bookings

## 🚀 Quick Start

1. **Setup:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Initialize Database:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

3. **Run:**
   ```bash
   python manage.py runserver
   ```

4. **Access:**
   - Home: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
Movie show Booking/
├── movie_booking/      # Project settings
├── movies/             # Main app (models, views, forms)
├── templates/          # HTML templates
├── static/             # CSS, images
├── media/              # Uploaded posters
└── requirements.txt
```

## 🗄️ Models

- **Movie** - Title, genre, rating, duration, poster
- **Theater** - Name, location, capacity
- **Show** - Movie, theater, showtime, price, seats
- **Booking** - User, show, seats, payment details

## 🛠️ Tech Stack

- Django 4.2+
- Bootstrap 5
- SQLite
- Pillow

## 👥 Team

- **Aman Kokate** - Team Leader ([GitHub](https://github.com/AmanKokate) | [LinkedIn](https://www.linkedin.com/in/aman-kokate/) | [Portfolio](https://amankokate.github.io/MyPortfolio/))
- **Kasturi Bhogal** - Frontend Manager
- **Aditya Hire** - Backend Manager

## 📧 Contact

amankokate1@gmail.com
