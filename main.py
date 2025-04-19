from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import database
from pydantic import BaseModel

app = FastAPI(title="Netflix Tarzı Öneri Sistemi")

# Pydantic modelleri
class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class ContentCreate(BaseModel):
    title: str
    type: str
    genre: str
    release_year: int

class ContentResponse(BaseModel):
    id: int
    title: str
    type: str
    genre: str
    release_year: int

    class Config:
        from_attributes = True

class WatchContent(BaseModel):
    user_id: int
    content_id: int
    rating: float

# Veritabanını başlat
database.init_db()

# Bağımlılıklar
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.post("/contents/", response_model=ContentResponse)
def create_content(content: ContentCreate, db: Session = Depends(get_db)):
    db_content = models.Content(
        title=content.title,
        type=content.type,
        genre=content.genre,
        release_year=content.release_year
    )
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

@app.get("/contents/", response_model=List[ContentResponse])
def get_contents(db: Session = Depends(get_db)):
    contents = db.query(models.Content).all()
    return contents

@app.post("/watch/")
def watch_content(watch: WatchContent, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == watch.user_id).first()
    content = db.query(models.Content).filter(models.Content.id == watch.content_id).first()
    
    if not user or not content:
        raise HTTPException(status_code=404, detail="Kullanıcı veya içerik bulunamadı")
    
    # İzleme geçmişini kaydet
    stmt = models.user_content_association.insert().values(
        user_id=watch.user_id,
        content_id=watch.content_id,
        rating=watch.rating
    )
    db.execute(stmt)
    db.commit()
    
    return {"message": "İzleme geçmişi kaydedildi"}

@app.get("/recommend/{user_id}")
def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    recommender = database.Recommender(db)
    recommender.fit()
    recommendations = recommender.recommend(user_id)
    
    return [
        {
            "id": content.id,
            "title": content.title,
            "type": content.type,
            "genre": content.genre,
            "release_year": content.release_year
        }
        for content in recommendations
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 