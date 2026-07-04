# MoodTune API 🎧

**MoodTune API** is a Python-based backend application (REST API) designed to personalize music experiences.

### Project Overview
The main goal of this service is to select and recommend music based on the user's current mood. The system analyzes user inputs and utilizes an integrated Machine Learning model (`ml_model.py`) to suggest the most suitable music tracks.

### Key Features
* **Authentication (`auth.py`)** - Secure user registration, login, and route protection.
* **Smart Recommendation (`ml_model.py`)** - Machine learning logic for analyzing mood and predicting tracks.
* **Database Management (`database.py`)** - Reliable data storage for user profiles, tracks, and history.
* **Database Migrations (`migrations/`)** - Automated database schema tracking via Alembic.
* **Automated Testing (`tests/`)** - Built-in test suite to ensure API reliability and stability.
