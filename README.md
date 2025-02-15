# PC-Party 🖥️

PC-Party to platforma społecznościowa stworzona dla entuzjastów komputerów, gdzie użytkownicy mogą dzielić się zdjęciami swoich setupów, modyfikacji PC i buildów komputerowych.

## 🌟 Funkcjonalności

### Główne funkcje
- 📸 Udostępnianie zdjęć setupów komputerowych
- 💬 Komentowanie i dyskusje
- ❤️ System polubień

### Funkcje techniczne
- 🔐 JWT Authentication
- 📝 REST API
- 📚 Swagger dokumentacja API
- 🔄 CORS wsparcie
- 🗃️ SQLAlchemy ORM

## 🛠️ Technologie

### Backend
- Python 3.9
- Flask Framework
- SQLAlchemy
- Flask-JWT-Extended
- Flask-Bcrypt
- Flask-CORS
- Flask-Swagger-UI

### Baza danych
- PostgreSQL

### Dokumentacja
- Swagger/OpenAPI 3.0

## 🚀 Instalacja i uruchomienie

### Wymagania
- Docker
- Docker Compose
- Git

### Uruchomienie z użyciem Dockera

1. Sklonuj repozytorium:bash
git clone https://github.com/Midop01/ZTPAI

2. Zbuduj i uruchom kontenery:
```bash
docker compose up --build
```

3. Aplikacja będzie dostępna pod adresem:
- Backend API: `http://localhost:5000`
- Dokumentacja API: `http://localhost:5000/api/docs`

### Manualna instalacja (development)

1. Stwórz i aktywuj środowisko wirtualne:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

2. Zainstaluj zależności:
```bash
pip install -r backend/requirements.txt
```

3. Uruchom aplikację:
```bash
cd backend
python app.py
```

## 📁 Struktura projektu

```
backend/
├── app.py              # Główny plik aplikacji
├── config.py           # Konfiguracja
├── extensions.py       # Rozszerzenia Flask
├── requirements.txt    # Zależności
├── swagger.yml         # Dokumentacja API
├── Dockerfile         
├── models/
│   ├── user.py        # Model użytkownika
│   └── post.py        # Model postu
└── routes/
    ├── auth.py        # Endpointy autoryzacji
    ├── comments.py    # Endpointy komentarzy
    └── images.py      # Endpointy obrazów
```

## 📌 API Endpoints

### Autoryzacja
- `POST /api/auth/register` - Rejestracja użytkownika
- `POST /api/auth/login` - Logowanie

### Posty
- `GET /api/posts` - Lista postów
- `POST /api/posts` - Utworzenie nowego postu
- `GET /api/posts/{id}` - Szczegóły postu
- `DELETE /api/posts/{id}` - Usunięcie postu

### Komentarze
- `GET /api/posts/{id}/comments` - Komentarze do postu
- `POST /api/posts/{id}/comments` - Dodanie komentarza

### Polubienia
- `POST /api/posts/{id}/like` - Polubienie postu
- `DELETE /api/posts/{id}/like` - Usunięcie polubienia

### Obrazy
- `POST /api/images/upload` - Upload zdjęcia

## 🔒 Bezpieczeństwo

- Hasła są hashowane przy użyciu bcrypt
- Autentykacja przez JWT tokens
- CORS jest skonfigurowany dla bezpiecznych domen
- Walidacja danych wejściowych
- Sanityzacja uploadowanych plików


## 💾 Schemat bazy danych

### User
| Kolumna        | Typ         | Opis                    |
|----------------|-------------|-------------------------|
| id             | INTEGER     | Klucz główny            |
| username       | VARCHAR(64) | Nazwa użytkownika       |
| email          | VARCHAR(120)| Adres email             |
| password_hash  | VARCHAR(128)| Zahashowane hasło       |
| created_at     | TIMESTAMP   | Data utworzenia konta   |

### Post
| Kolumna        | Typ         | Opis                    |
|----------------|-------------|-------------------------|
| id             | INTEGER     | Klucz główny            |
| title          | VARCHAR(100)| Tytuł postu             |
| content        | TEXT        | Opis setupu             |
| image_data     | Large Binary| Zdjęcie                 |
| image_name     | VARCHAR(256)| Nazwa zdjęcia           |
| author_id      | INTEGER     | FK -> User.id           |
| created_at     | TIMESTAMP   | Data utworzenia         |

### Comment
| Kolumna        | Typ         | Opis                    |
|----------------|-------------|-------------------------|
| id             | INTEGER     | Klucz główny            |
| content        | TEXT        | Treść komentarza        |
| author_id      | INTEGER     | FK -> User.id           |
| post_id        | INTEGER     | FK -> Post.id           |
| created_at     | TIMESTAMP   | Data utworzenia         |

### Like
| Kolumna        | Typ         | Opis                    |
|----------------|-------------|-------------------------|
| user_id        | INTEGER     | FK -> User.id           |
| post_id        | INTEGER     | FK -> Post.id           |

### Relacje

- User 1:N Post (Jeden użytkownik może mieć wiele postów)
- User 1:N Comment (Jeden użytkownik może mieć wiele komentarzy)
- Post 1:N Comment (Jeden post może mieć wiele komentarzy)
- User N:M Post (poprzez Like - użytkownik może lubić wiele postów)

### Indeksy
- User: email (unique), username (unique)
- Post: author_id, created_at
- Comment: post_id, author_id
- Like: (user_id, post_id) unique
- Tag: name (unique)

## 👥 Autorzy

- Michał Buchała - [GitHub](https://github.com/Midop01)