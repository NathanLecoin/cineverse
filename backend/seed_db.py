"""
Script to seed the database with popular movies
Run this after init_db.py to populate sample data
"""
from app.db.session import SessionLocal
from app.models.movie import Movie

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
        }
    ]
    
    # Vérifier si les films existent déjà
    existing_count = db.query(Movie).count()
    
    if existing_count > 0:
        print(f"⚠️  Database already contains {existing_count} movies. Skipping seed.")
        db.close()
        return
    
    for movie_data in movies_data:
        movie = Movie(**movie_data)
        db.add(movie)
    
    db.commit()
    print(f"✅ Successfully seeded {len(movies_data)} movies!")
    db.close()

if __name__ == "__main__":
    seed_movies()
