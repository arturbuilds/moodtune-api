import pytest
import json
from httpx import AsyncClient, ASGITransport
from main import app, redis_client

@pytest.fixture(autouse=True)
def mock_redis(monkeypatch):
    fake_storage = {}

    async def mock_get(key):
        return fake_storage.get(key)

    async def mock_set(key, value, *args, **kwargs):
        fake_storage[key] = value
        return True

    async def mock_aclose():
        pass

    monkeypatch.setattr(redis_client, "get", mock_get)
    monkeypatch.setattr(redis_client, "set", mock_set)
    monkeypatch.setattr(redis_client, "aclose", mock_aclose)

@pytest.mark.asyncio
async def test_recommend_endpoint_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        response = await ac.get('/recommend?q=хочу тренироваться в зале')

        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'success'
        assert data['source'] in ['ai_model', 'cached']
        assert 'title' in data['track']

@pytest.mark.asyncio
async def test_recommend_endpoint_too_short():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get('/recommend?q=хо')
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_recommend_endpoint_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        response = await ac.get('/recommend?q=абрвалг хддд лол')
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_redis_cache_logic():
    test_key = f'vibe:тестовый_запрос_для_теста'
    fake_track_data = {'id': 99, 'title': 'Test Fake Track', 'vibe': 'тест'}

    await redis_client.set(test_key, json.dumps(fake_track_data), ex=10)

    cached_data = await redis_client.get(test_key)
    assert cached_data is not None

    parsed_json = json.loads(cached_data)
    assert parsed_json['title'] == 'Test Fake Track'

    await redis_client.delete(test_key)