"""
Script to seed the database with popular movies, users, reviews and watchlists
Run this after init_db.py to populate sample data
"""
from app.db.session import SessionLocal
from app.models.movie import Movie
from app.models.user import User
from app.models.review import Review
from app.models.watchlist import Watchlist
from app.core.security import get_password_hash

def seed_movies():
    db = SessionLocal()
    
    movies_data = [
        {
            "title": "Inception",
            "description": "Un voleur qui vole les secrets des rêves des gens pendant leur sommeil.",
            "release_year": 2010
        },
        {
            "title": "The Matrix",
            "description": "Un hacker découvre la vérité sur sa réalité et son rôle dans la guerre contre ses contrôleurs.",
            "release_year": 1999
        },
        {
            "title": "Interstellar",
            "description": "Un groupe d'explorateurs voyagent à travers un trou de ver près de Saturne à la recherche d'une nouvelle maison pour l'humanité.",
            "release_year": 2014
        },
        {
            "title": "The Dark Knight",
            "description": "Quand la menace connue sous le nom de Joker dévaste et plonge Gotham dans l'anarchie, Batman doit accepter l'une des épreuves psychologiques et physiques les plus difficiles.",
            "release_year": 2008
        },
        {
            "title": "Pulp Fiction",
            "description": "Les vies de deux tueurs à gages, d'un gangster et de sa femme, et d'un couple de braqueurs s'entrelacent dans quatre récits de violence et de rédemption.",
            "release_year": 1994
        },
        {
            "title": "The Shawshank Redemption",
            "description": "Deux hommes condamnés à la prison à vie nouent une amitié profonde sur un nombre d'années, trouvant du réconfort et de la rédemption par une série d'actes de bonté.",
            "release_year": 1994
        },
        {
            "title": "Forrest Gump",
            "description": "Les exploits d'un homme avec un faible QI mais une volonté inébranlable car il maîtrise plusieurs domaines de sa vie et inspire ses entourage.",
            "release_year": 1994
        },
        {
            "title": "The Godfather",
            "description": "Le film suit la famille Corleone dirigée par Vito Corleone, le patriarche d'une famille organisée de la mafia la plus puissante.",
            "release_year": 1972
        },
        {
            "title": "Titanic",
            "description": "Un conte d'amour et de tragédie se déroule alors que deux passagers de classe différente tombent amoureux à bord du RMS Titanic.",
            "release_year": 1997
        },
        {
            "title": "Avengers: Endgame",
            "description": "Après les événements dévastateurs, les Avengers se réunissent pour un combat final contre Thanos.",
            "release_year": 2019
        },
        {
            "title": "Avatar",
            "description": "Un paraplégique qui est Marine s'infiltre dans une colonie extraterrestre pour espionner les Na'vi.",
            "release_year": 2009
        },
        {
            "title": "Oppenheimer",
            "description": "La vie du physicien J. Robert Oppenheimer et son rôle dans le développement de la bombe atomique.",
            "release_year": 2023
        },
        {
            "title": "The Lion King",
            "description": "Le fils d'un roi lion fuit son royaume après la mort de son père et découvre le pouvoir de vivre en exil.",
            "release_year": 1994
        },
        {
            "title": "Dune",
            "description": "Paul Atreides, le fils d'un noble dirigeant, doit voyager pour la planète la plus dangereuse de l'univers pour assurer l'avenir de sa famille et de la race humaine.",
            "release_year": 2021
        },
        {
            "title": "Fight Club",
            "description": "Un employé insomniaque et un savonnier capitaliste forment un club de combat souterrain qui progresse en quelque chose de beaucoup plus grand.",
            "release_year": 1999
        },
        {
            "title": "Parasite",
            "description": "Greed et classe dans la Corée du Sud collent une famille pauvre à la maison, ce qui les porte à soutirer un plan ambitieux.",
            "release_year": 2019
        },
        {
            "title": "The Silence of the Lambs",
            "description": "Un agent du FBI en détresse consulte le meurtrier en série en prison pour attraper un autre tueur en série qui peau ses victimes.",
            "release_year": 1991
        },
        {
            "title": "Gladiator",
            "description": "Un ancien général romain est réduit en esclavage après la mort de son fils par l'ambition du nouvel empereur.",
            "release_year": 2000
        },
        {
            "title": "The Usual Suspects",
            "description": "Cinq braqueurs de banque apparemment sans lien sont amenés ensemble pour une enquête sur un navire criminel mystérieux.",
            "release_year": 1995
        },
        {
            "title": "Joker",
            "description": "Un comédien de seconde classe en crise mentale et en marginalisation sociale crée un personnage de tueur en série.",
            "release_year": 2019
        },
        {
            "title": "Blade Runner 2049",
            "description": "Un jeune blade runner découvre un secret longtemps enterré qui a le potentiel de plonger ce qui reste de la société dans le chaos.",
            "release_year": 2017
        },
        {
            "title": "The Lord of the Rings: The Fellowship of the Ring",
            "description": "Un hobbit modeste de la Comté et huit compagnons entreprennent un voyage pour détruire le puissant Anneau Unique.",
            "release_year": 2001
        },
        {
            "title": "Spider-Man: Into the Spider-Verse",
            "description": "Miles Morales devient Spider-Man et rejoint d'autres Spider-People de différentes dimensions.",
            "release_year": 2018
        },
        {
            "title": "Whiplash",
            "description": "Un jeune batteur ambitieux de jazz fait face à un professeur abusif dans une prestigieuse école de musique.",
            "release_year": 2014
        },
        {
            "title": "La La Land",
            "description": "Une actrice en herbe et un musicien de jazz passionné tombent amoureux tout en poursuivant leurs rêves à Los Angeles.",
            "release_year": 2016
        },
        {
            "title": "Mad Max: Fury Road",
            "description": "Dans un monde post-apocalyptique, Max s'associe à Furiosa pour échapper à un culte tyrannique.",
            "release_year": 2015
        },
        {
            "title": "Get Out",
            "description": "Un jeune homme afro-américain rend visite à la famille de sa petite amie blanche et découvre un secret terrifiant.",
            "release_year": 2017
        },
        {
            "title": "The Grand Budapest Hotel",
            "description": "Les aventures de Gustave H, un concierge légendaire dans un hôtel européen célèbre.",
            "release_year": 2014
        },
        {
            "title": "Coco",
            "description": "Un jeune garçon aspirant musicien se retrouve dans le Pays des Morts et cherche l'aide de son arrière-arrière-grand-père.",
            "release_year": 2017
        },
        {
            "title": "1917",
            "description": "Deux jeunes soldats britanniques doivent traverser le territoire ennemi pour délivrer un message vital.",
            "release_year": 2019
        }
    ]
    
    existing_count = db.query(Movie).count()
    
    if existing_count > 0:
        print(f"Database already contains {existing_count} movies. Skipping seed.")
        db.close()
        return
    
    for movie_data in movies_data:
        movie = Movie(**movie_data)
        db.add(movie)
    
    db.commit()
    print(f"Successfully seeded {len(movies_data)} movies!")
    db.close()

def seed_admin_user():
    """Create an admin user if it doesn't exist"""
    db = SessionLocal()
    
    # Check if admin user already exists
    existing_admin = db.query(User).filter(User.username == "admin").first()
    
    if existing_admin:
        print("Admin user already exists. Skipping.")
        db.close()
        return
    
    # Create admin user
    admin_user = User(
        username="admin",
        email="admin@cineverse.fr",
        full_name="Administrator",
        hashed_password=get_password_hash("adminpassword123"),
        is_active=True,
        is_admin=True
    )
    
    db.add(admin_user)
    db.commit()
    print("Admin user created! (username: admin, password: adminpassword123)")
    db.close()


def seed_users():
    """Create Alice and Bob users for demo"""
    db = SessionLocal()
    
    # Check if users exist
    alice_exists = db.query(User).filter(User.username == "alice").first()
    bob_exists = db.query(User).filter(User.username == "bob").first()
    
    users_created = 0
    
    if not alice_exists:
        alice = User(
            username="alice",
            email="alice@cineverse.fr",
            full_name="Alice Dupont",
            hashed_password=get_password_hash("alice123"),
            is_active=True,
            is_admin=False
        )
        db.add(alice)
        users_created += 1
    
    if not bob_exists:
        bob = User(
            username="bob",
            email="bob@cineverse.fr",
            full_name="Bob Martin",
            hashed_password=get_password_hash("bob123"),
            is_active=True,
            is_admin=False
        )
        db.add(bob)
        users_created += 1
    
    if users_created > 0:
        db.commit()
        print(f"Successfully created {users_created} users (Alice and Bob)!")
    else:
        print("Users Alice and Bob already exist. Skipping.")
    
    db.close()


def seed_reviews():
    """Create reviews by Alice and Bob"""
    db = SessionLocal()
    
    alice = db.query(User).filter(User.username == "alice").first()
    bob = db.query(User).filter(User.username == "bob").first()
    
    if not alice or not bob:
        print("Warning: Alice or Bob user not found. Cannot seed reviews.")
        db.close()
        return
    
    reviews_data = [
        # Alice's reviews
        {"user_id": alice.id, "movie_id": 1, "rating": 5, "comment": "Chef-d'œuvre absolu ! Inception m'a complètement bluffée. La complexité des niveaux de rêves est fascinante."},
        {"user_id": alice.id, "movie_id": 2, "rating": 5, "comment": "Matrix a révolutionné le cinéma de science-fiction. Une philosophie profonde cachée dans un film d'action."},
        {"user_id": alice.id, "movie_id": 3, "rating": 4, "comment": "Interstellar est visuellement magnifique mais un peu long. Les scènes spatiales sont incroyables."},
        {"user_id": alice.id, "movie_id": 8, "rating": 5, "comment": "Le Parrain reste le meilleur film de tous les temps. Un chef-d'œuvre du cinéma."},
        {"user_id": alice.id, "movie_id": 12, "rating": 4, "comment": "Oppenheimer est intense et historiquement fascinant. Nolan au sommet de son art."},
        {"user_id": alice.id, "movie_id": 16, "rating": 5, "comment": "Parasite est une critique sociale brillante. Un film coréen qui mérite tous ses Oscars."},
        {"user_id": alice.id, "movie_id": 25, "rating": 4, "comment": "La La Land est un hommage magnifique aux comédies musicales classiques avec une fin mélancolique."},
        
        # Bob's reviews
        {"user_id": bob.id, "movie_id": 4, "rating": 5, "comment": "Heath Ledger est incroyable en Joker ! Une performance inoubliable qui transcende le film de super-héros."},
        {"user_id": bob.id, "movie_id": 5, "rating": 4, "comment": "Pulp Fiction est culte, mais pas pour tout le monde. Tarantino à son meilleur."},
        {"user_id": bob.id, "movie_id": 6, "rating": 5, "comment": "Un film qui donne espoir, j'ai adoré. Morgan Freeman et Tim Robbins sont parfaits."},
        {"user_id": bob.id, "movie_id": 10, "rating": 3, "comment": "Avengers c'est fun mais un peu trop de CGI à mon goût. Divertissant mais prévisible."},
        {"user_id": bob.id, "movie_id": 15, "rating": 5, "comment": "Fight Club est un film qui fait réfléchir sur la société moderne. Le twist final est légendaire."},
        {"user_id": bob.id, "movie_id": 20, "rating": 4, "comment": "Joaquin Phoenix est troublant dans ce rôle. Une vision sombre et réaliste du personnage."},
        {"user_id": bob.id, "movie_id": 26, "rating": 5, "comment": "Mad Max Fury Road est une symphonie visuelle. Action pure du début à la fin!"},
    ]
    
    reviews_created = 0
    
    for review_data in reviews_data:
        existing = db.query(Review).filter(
            Review.user_id == review_data["user_id"],
            Review.movie_id == review_data["movie_id"]
        ).first()
        
        if not existing:
            review = Review(**review_data)
            db.add(review)
            reviews_created += 1
    
    if reviews_created > 0:
        db.commit()
        print(f"Successfully seeded {reviews_created} reviews!")
    else:
        print("Reviews already exist. Skipping.")
    
    db.close()


def seed_watchlists():
    """Create watchlist entries for Alice and Bob"""
    db = SessionLocal()
    
    alice = db.query(User).filter(User.username == "alice").first()
    bob = db.query(User).filter(User.username == "bob").first()
    
    if not alice or not bob:
        print("Warning: Alice or Bob user not found. Cannot seed watchlists.")
        db.close()
        return
    
    watchlist_data = [
        # Alice's watchlist - films she wants to watch
        {"user_id": alice.id, "movie_id": 7},   # Forrest Gump
        {"user_id": alice.id, "movie_id": 11},  # Avatar
        {"user_id": alice.id, "movie_id": 14},  # Dune
        {"user_id": alice.id, "movie_id": 22},  # The Lord of the Rings
        {"user_id": alice.id, "movie_id": 28},  # The Grand Budapest Hotel
        
        # Bob's watchlist - films he wants to watch
        {"user_id": bob.id, "movie_id": 9},    # Titanic
        {"user_id": bob.id, "movie_id": 13},   # Lion King
        {"user_id": bob.id, "movie_id": 17},   # Silence of the Lambs
        {"user_id": bob.id, "movie_id": 18},   # Gladiator
        {"user_id": bob.id, "movie_id": 23},   # Spider-Man: Into the Spider-Verse
        {"user_id": bob.id, "movie_id": 29},   # Coco
    ]
    
    watchlist_created = 0
    
    for wl_data in watchlist_data:
        existing = db.query(Watchlist).filter(
            Watchlist.user_id == wl_data["user_id"],
            Watchlist.movie_id == wl_data["movie_id"]
        ).first()
        
        if not existing:
            watchlist = Watchlist(**wl_data)
            db.add(watchlist)
            watchlist_created += 1
    
    if watchlist_created > 0:
        db.commit()
        print(f"Successfully seeded {watchlist_created} watchlist entries!")
    else:
        print("Watchlist entries already exist. Skipping.")
    
    db.close()


if __name__ == "__main__":
    seed_movies()
    seed_admin_user()
    seed_users()
    seed_reviews()
    seed_watchlists()
