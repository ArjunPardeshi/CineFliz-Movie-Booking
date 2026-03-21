import sqlite3
import os
import urllib.request
import urllib.parse

print("Starting the automated Database Seeder...")

os.makedirs('posters', exist_ok=True)

conn = sqlite3.connect('cinema.db')
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS Movies")
c.execute("DROP TABLE IF EXISTS Showtimes")
c.execute("DROP TABLE IF EXISTS Bookings")

# UPDATED: Added trailer_url and review_url columns
c.execute("CREATE TABLE Movies (id INTEGER PRIMARY KEY, title TEXT, genre TEXT, poster_url TEXT, cities TEXT, trailer_url TEXT, review_url TEXT)")
c.execute("CREATE TABLE Showtimes (id INTEGER PRIMARY KEY, movie_id INTEGER, show_time TEXT)")
c.execute("CREATE TABLE Bookings (id INTEGER PRIMARY KEY AUTOINCREMENT, showtime_id INTEGER, seat_number TEXT, customer_name TEXT)")

movies_data = [
    (1, "Dhurandhar The Revenge", "Action/Drama", "Pune, Mumbai, Delhi, Bangalore, Wardha, Nashik, Sangamner", "https://youtu.be/NHk7scrb_9I", "https://www.moctale.in/content/dhurandhar-the-revenge-2026"),
    (2, "Bhooth Bangla", "Horror/Comedy", "Pune, Mumbai, Delhi, Bangalore, Wardha, Nashik, Sangamner", "https://youtu.be/x0aMsjhFxeE", "https://www.moctale.in/content/bhooth-bangla-2026"),
    (3, "Ustaad Bhagat Singh", "Action/Romance", "Pune, Mumbai, Delhi, Bangalore, Wardha, Nashik, Sangamner", "https://youtu.be/MLU5ZEp9YDo", "https://www.moctale.in/content/ustaad-bhagat-singh-2026"),
    (4, "That Time I Got Reincarnated as a Slime the Movie: Tears of the Azure Sea", "Anime/Fantasy", "Pune, Nashik, Bangalore", "https://youtu.be/RBJL4B0abpI", "https://www.imdb.com/title/tt38650409/"),
    (5, "The Super Mario Galaxy Movie", "Animation/Adventure", "Pune, Nashik, Bangalore", "https://youtu.be/EbYtRe6dgMs", "https://www.moctale.in/content/the-super-mario-galaxy-movie-2026")
]

db_movies = []

# FIXED: Unpack all 6 variables to avoid the ValueError, and removed the auto-generation logic
for m_id, title, genre, cities, trailer_url, review_url in movies_data:
    local_filename = f"posters/movie_{m_id}.jpg"
    safe_title = urllib.parse.quote_plus(title)
    fallback_url = f"https://placehold.co/500x750/000000/E50914/png?text={safe_title}"
    
    try:
        if not os.path.exists(local_filename):
            req = urllib.request.Request(fallback_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(local_filename, 'wb') as out_file:
                out_file.write(response.read())
    except Exception as e:
        pass
        
    db_movies.append((m_id, title, genre, local_filename, cities, trailer_url, review_url))

# Insert into the updated table
c.executemany("INSERT INTO Movies VALUES (?, ?, ?, ?, ?, ?, ?)", db_movies)

showtimes = [
    (1, 1, "Today at 10:30 AM"), (2, 1, "Today at 2:15 PM"),
    (3, 2, "Today at 11:45 AM"), (4, 2, "Today at 5:30 PM"),
    (5, 3, "Today at 1:00 PM"),  (6, 3, "Today at 8:45 PM"),
    (7, 4, "Today at 12:00 PM"), (8, 4, "Today at 6:15 PM"),
    (9, 5, "Today at 9:30 AM"),  (10, 5, "Today at 4:45 PM")
]
c.executemany("INSERT INTO Showtimes VALUES (?, ?, ?)", showtimes)

conn.commit()
print("\nSuccess! Database seeded with custom Trailer and Review links.")