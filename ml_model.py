from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import HTTPException
import numpy as np
import pymorphy3

morph = pymorphy3.MorphAnalyzer()

def clean_text(text: str) -> str:
    words = text.lower().split()
    clean_words = []
    for word in words:
        word = word.strip(".,!?()-\"")
        parsed = morph.parse(word)[0]
        clean_words.append(parsed.normal_form)
    return " ".join(clean_words)

def get_recommendation(user_query: str, tracks_from_db: list):
    if not tracks_from_db:
        raise HTTPException(status_code=404, detail="В базе данных еще нет треков. Сначала добавь их через POST!")

    vectorizer = TfidfVectorizer()

    description = [clean_text(track.vibe) for track in tracks_from_db]
    tfidf_matrix = vectorizer.fit_transform(description)

    cleaned_query = clean_text(user_query)
    query_vector = vectorizer.transform([cleaned_query])
    
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

    if np.all(similarities == 0):
        return None

    best_match_index = np.argmax(similarities)

    best_track = tracks_from_db[best_match_index]

    return {
        "id": best_track.id,
        "title": best_track.title,
        "artist": best_track.artist,
        "vibe": best_track.vibe
    }