# Netflix Tarzı Film/Dizi Öneri Sistemi

Bu proje, kullanıcıların izleme geçmişine ve puanlarına göre film ve dizi önerileri sunan bir öneri sistemidir. KMeans kümeleme algoritması kullanılarak benzer izleme alışkanlıklarına sahip kullanıcılar gruplandırılır ve bu gruplardaki diğer kullanıcıların izlediği içerikler önerilir.

## Özellikler

- Kullanıcı ve içerik yönetimi
- İzleme geçmişi ve puanlama sistemi
- KMeans tabanlı öneri motoru
- FastAPI ile REST API
- SQLite veritabanı
- SQLAlchemy ORM

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Veritabanını ve örnek verileri oluşturun:
```bash
python seed_data.py
```

3. FastAPI uygulamasını başlatın:
```bash
python main.py
```

Uygulama http://localhost:8000 adresinde çalışacaktır.

## API Endpoint'leri

### Kullanıcı İşlemleri
- `POST /users/`: Yeni kullanıcı oluşturma
```json
{
    "username": "kullanici_adi",
    "email": "email@example.com"
}
```

### İçerik İşlemleri
- `POST /contents/`: Yeni içerik ekleme
```json
{
    "title": "Film/Dizi Adı",
    "type": "movie/series",
    "genre": "Tür",
    "release_year": 2023
}
```

### İzleme İşlemleri
- `POST /watch/`: İzleme geçmişi kaydetme
```json
{
    "user_id": 1,
    "content_id": 1,
    "rating": 4.5
}
```

### Öneri Sistemi
- `GET /recommend/{user_id}`: Kullanıcı için öneriler getirme

## Örnek Kullanım

1. Yeni bir kullanıcı oluşturun:
```bash
curl -X POST "http://localhost:8000/users/" -H "Content-Type: application/json" -d '{"username":"test_user","email":"test@example.com"}'
```

2. Yeni bir içerik ekleyin:
```bash
curl -X POST "http://localhost:8000/contents/" -H "Content-Type: application/json" -d '{"title":"Test Film","type":"movie","genre":"Aksiyon","release_year":2023}'
```

3. İzleme geçmişi kaydedin:
```bash
curl -X POST "http://localhost:8000/watch/" -H "Content-Type: application/json" -d '{"user_id":1,"content_id":1,"rating":4.5}'
```

4. Önerileri alın:
```bash
curl "http://localhost:8000/recommend/1"
```

## API Dokümantasyonu

API dokümantasyonuna http://localhost:8000/docs adresinden erişebilirsiniz.

## Proje Yapısı

- `models.py`: Veritabanı modelleri
- `database.py`: Veritabanı bağlantısı ve öneri motoru
- `main.py`: FastAPI uygulaması
- `seed_data.py`: Örnek veri oluşturma scripti
- `requirements.txt`: Gerekli Python paketleri

## Geliştirici

Bu proje [Geliştirici Adı] tarafından geliştirilmiştir. 