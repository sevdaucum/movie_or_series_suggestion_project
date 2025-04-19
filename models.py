from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# Kullanıcı ve içerik arasındaki ilişki tablosu
user_content_association = Table(
    'user_content_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('content_id', Integer, ForeignKey('contents.id')),
    Column('rating', Float),
    Column('watched_at', DateTime, default=datetime.utcnow)
)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    watched_contents = relationship(
        "Content",
        secondary=user_content_association,
        back_populates="watched_by"
    )

class Content(Base):
    __tablename__ = 'contents'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False)  # 'movie' veya 'series'
    genre = Column(String(50), nullable=False)
    release_year = Column(Integer)
    watched_by = relationship(
        "User",
        secondary=user_content_association,
        back_populates="watched_contents"
    ) 