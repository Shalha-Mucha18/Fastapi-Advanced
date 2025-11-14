import aioredis
from src.config import Config

JWT_EXPIRY = 3600

token_blocklist = aioredis.StrictRedis(
    host=Config.REDIS_HOST,
port=Config.REDIS_PORT, db=0, decode_responses=True

)

async def add_jti_to_blocklist(jti: str):
    await token_blocklist.set(name = jti, value="revoked", ex=JWT_EXPIRY)


async def token_in_blocklist(jti: str) -> bool:
    jti = await token_blocklist.get(name = jti)
    return jti is not None    
