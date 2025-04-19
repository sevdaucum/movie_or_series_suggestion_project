from sqlalchemy.orm import Session
import models
import database

def seed_data():
    db = database.SessionLocal()
    
    # Örnek kullanıcılar
    users = [
        models.User(username="ahmet", email="ahmet@example.com"),
        models.User(username="mehmet", email="mehmet@example.com"),
        models.User(username="ayse", email="ayse@example.com"),
        models.User(username="fatma", email="fatma@example.com")
    ]
    
    # Örnek içerikler
    contents = [
        models.Content(title="Inception", type="movie", genre="Bilim Kurgu", release_year=2010),
        models.Content(title="The Dark Knight", type="movie", genre="Aksiyon", release_year=2008),
        models.Content(title="Breaking Bad", type="series", genre="Drama", release_year=2008),
        models.Content(title="Stranger Things", type="series", genre="Bilim Kurgu", release_year=2016),
        models.Content(title="The Office", type="series", genre="Komedi", release_year=2005),
        models.Content(title="Pulp Fiction", type="movie", genre="Suç", release_year=1994),
        models.Content(title="The Matrix", type="movie", genre="Bilim Kurgu", release_year=1999),
        models.Content(title="Friends", type="series", genre="Komedi", release_year=1994)
    ]
    
    # Veritabanına ekle
    for user in users:
        db.add(user)
    for content in contents:
        db.add(content)
    
    db.commit()
    
    # Örnek izleme geçmişi
    watch_history = [
        (1, 1, 4.5),  # ahmet -> Inception
        (1, 2, 5.0),  # ahmet -> The Dark Knight
        (2, 3, 4.8),  # mehmet -> Breaking Bad
        (2, 4, 4.2),  # mehmet -> Stranger Things
        (3, 5, 4.0),  # ayse -> The Office
        (3, 6, 4.7),  # ayse -> Pulp Fiction
        (4, 7, 4.9),  # fatma -> The Matrix
        (4, 8, 4.3)   # fatma -> Friends
    ]
    
    for user_id, content_id, rating in watch_history:
        stmt = models.user_content_association.insert().values(
            user_id=user_id,
            content_id=content_id,
            rating=rating
        )
        db.execute(stmt)
    
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_data()
    print("Örnek veriler başarıyla eklendi!") 