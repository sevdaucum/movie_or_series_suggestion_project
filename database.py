from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Base, User, Content
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from fastapi import HTTPException

# SQLite veritabanı bağlantısı
SQLALCHEMY_DATABASE_URL = "sqlite:///./netflix_recommender.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Recommender:
    def __init__(self, db):
        self.db = db
        self.kmeans = KMeans(n_clusters=5, random_state=42)
        
    def prepare_data(self):
        # Kullanıcı-İçerik matrisini oluştur
        users = self.db.query(User).all()
        contents = self.db.query(Content).all()
        
        if not users or not contents:
            raise HTTPException(status_code=404, detail="Yeterli veri bulunamadı")
        
        # Boş bir matris oluştur
        user_content_matrix = np.zeros((len(users), len(contents)))
        
        # Kullanıcıların izlediği içerikleri ve puanlarını doldur
        for user in users:
            for content in user.watched_contents:
                user_idx = users.index(user)
                content_idx = contents.index(content)
                # İzleme geçmişinden puanı al
                rating = self.db.execute(
                    text("SELECT rating FROM user_content_association WHERE user_id = :user_id AND content_id = :content_id"),
                    {"user_id": user.id, "content_id": content.id}
                ).scalar()
                user_content_matrix[user_idx, content_idx] = rating or 0
        
        return user_content_matrix, users, contents
    
    def fit(self):
        try:
            user_content_matrix, _, _ = self.prepare_data()
            if len(user_content_matrix) < 2:  # En az 2 kullanıcı olmalı
                raise HTTPException(status_code=400, detail="Öneri için yeterli kullanıcı verisi yok")
            self.kmeans.fit(user_content_matrix)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Öneri sistemi hatası: {str(e)}")
    
    def recommend(self, user_id, n_recommendations=5):
        try:
            user_content_matrix, users, contents = self.prepare_data()
            
            # Kullanıcının indeksini bul
            user_idx = next((i for i, user in enumerate(users) if user.id == user_id), None)
            if user_idx is None:
                raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
            
            # Kullanıcının kümesini bul
            user_cluster = self.kmeans.labels_[user_idx]
            
            # Aynı kümedeki diğer kullanıcıları bul
            similar_users = [i for i, label in enumerate(self.kmeans.labels_) if label == user_cluster and i != user_idx]
            
            if not similar_users:
                # Eğer benzer kullanıcı yoksa, en popüler içerikleri öner
                all_contents = self.db.query(Content).all()
                return all_contents[:n_recommendations]
            
            # Benzer kullanıcıların izlediği içerikleri topla
            recommendations = []
            for user_idx in similar_users:
                user = users[user_idx]
                for content in user.watched_contents:
                    if content not in users[user_idx].watched_contents:
                        recommendations.append(content)
            
            # Tekrarlanan önerileri kaldır ve sırala
            unique_recommendations = list(set(recommendations))
            return unique_recommendations[:n_recommendations]
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Öneri oluşturma hatası: {str(e)}")