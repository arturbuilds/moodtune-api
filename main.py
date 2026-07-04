from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from contextlib import asynccontextmanager
import redis.asyncio as redis
import json
import os
from dotenv import load_dotenv
load_dotenv()

from database import get_async_db, engine, Base
from auth import create_access_token, get_current_user_id
import models
from ml_model import get_recommendation

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

redis_client = redis.Redis(
    host=os.getenv('redis_host'),
    port=6379,
    password=os.getenv('redis_password'),
    ssl=True,
    decode_responses=True
)

@app.post('/login')
def login():
    token = create_access_token(user_id=7)
    return {'access_token': token, 'token_type': 'bearer'}

@app.post('/tracks')
async def create_track(title: str, artist: str, vibe: str, db: AsyncSession = Depends(get_async_db)):
    new_track = models.Track(title=title, artist=artist, vibe=vibe)

    db.add(new_track)
    await db.commit()
    await db.refresh(new_track)

    return {'status': 'success', 'added': new_track.title}

@app.get('/recommend')
async def recommend_tracks(db: AsyncSession = Depends(get_async_db), user_id: int = Depends(get_current_user_id), q: str = Query(..., min_length=3, description="Твое настроение")):
    db_result = await db.execute(select(models.Track))
    tracks_from_db = db_result.scalars().all()
    
    cache_key = f'vibe:{q.strip().lower()}'
    cached_data = await redis_client.get(cache_key)

    if cached_data:
        data = json.loads(cached_data)
        return {'status': 'success', 'source': 'cached', 'track': data}
    
    result = get_recommendation(q, tracks_from_db)

    if result:
        await redis_client.set(cache_key, json.dumps(result), ex=300)
        return {'status': 'success', 'track': result, 'source': 'ai_model'}
    else:
        raise HTTPException(status_code=404, detail='ИИ не нашёл подходящих треков')