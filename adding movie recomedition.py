import random

# Movie database
movies = [
    {"title": "Inception", "genre": "Sci-Fi", "rating": 8.8, "mood": "mind-bending"},
    {"title": "The Dark Knight", "genre": "Action", "rating": 9.0, "mood": "intense"},
    {"title": "Interstellar", "genre": "Sci-Fi", "rating": 8.6, "mood": "emotional"},
    {"title": "La La Land", "genre": "Romance", "rating": 8.0, "mood": "uplifting"},
    {"title": "The Matrix", "genre": "Sci-Fi", "rating": 8.7, "mood": "philosophical"},
    {"title": "Toy Story", "genre": "Animation", "rating": 8.3, "mood": "happy"},
]

# Random recommendation
def recommend_random():
    return random.choice(movies)

# Genre-based recommendation
def recommend_genre(genre):
    filtered = [m for m in movies if m["genre"].lower() == genre.lower()]
    return random.choice(filtered) if filtered else None

# Mood-based recommendation
def recommend_mood(mood):
    filtered = [m for m in movies if m["mood"].lower() == mood.lower()]
    return random.choice(filtered) if filtered else None

# Rating-based recommendation
def recommend_rating(min_rating):
    filtered = [m for m in movies if m["rating"] >= min_rating]
    return random.choice(filtered) if filtered else None

# Examples
print("Random:", recommend_random())
print("Genre:", recommend_genre("Sci-Fi"))
print("Mood:", recommend_mood("happy"))
print("Rating:", recommend_rating(8.5))
