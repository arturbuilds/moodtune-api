import os
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dotenv import load_dotenv
import jwt

load_dotenv()

secret_key = os.getenv('jwt_secret_key', 'super-secret-key-123-xyz')
algorithm = 'HS256'

security = HTTPBearer()

def create_access_token(user_id: int, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    payload = {
        'sub': str(user_id),
        'exp': expire
    }

    encode_jwt = jwt.encode(payload, secret_key, algorithm=algorithm)
    return encode_jwt

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Security(security)) -> int:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        user_id: str = payload.get('sub')

        if user_id is None:
            raise HTTPException(status_code=401, detail='Неверный токен')
        
        return int(user_id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Время действия токена истекло')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Токен поврежден или недействителен')