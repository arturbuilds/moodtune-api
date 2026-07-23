# MoodTune API

Backend API for the MoodTune music application.

## Features

- User authentication
- JWT authorization
- User management
- REST API
- FastAPI backend
- Asynchronous architecture

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT
- Pydantic
- Uvicorn

## Installation

```bash
git clone https://github.com/arturbuilds/moodtune-api.git
cd moodtune-api

pip install -r requirements.txt
```

## Run

```bash
python main.py
```

or

```bash
uvicorn main:app --reload
```

## API Endpoints

### Authentication

```
POST /tracks
POST /login
GET /recommend
```

### User

```
GET /me
PUT /me
```

### Music

```
GET /tracks
GET /playlists
POST /favorites
```

## Project Structure

```
moodtune-api/
│
├── routers/
├── models/
├── schemas/
├── database.py
├── main.py
├── requirements.txt
└── README.md
```

## Future Improvements

- PostgreSQL
- Docker
- Redis
- Unit Tests
- CI/CD
