import httpx
from app.core.config import settings

class AuthServiceClient:
    def __init__(self):
        self.base_url = settings.AUTH_SERVICE_URL
        self.timeout = 3.0
    async def verify_token(self, token:str)->dict:
        payload = {
            "token":token,
            "internal_secret":settings.INTERNAL_SECRET
        }
        try:
            async with httpx.AsyncClient(timeout = self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/auth/verify-token",
                    json = payload
                )
                response.raise_for_status()
                return response.json()
        except httpx.TimeoutException:
            return {"valid":False,"error":"Auth Service Timeout"}
        except httpx.HTTPError as e:
            return {"valid":False, "error":str(e)}
        
    async def get_user(self, user_id:int)->dict:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                     f"{self.base_url}/auth/users/{user_id}",
                    headers={"X-Internal-Secret": settings.INTERNAL_SECRET}
                )
                response.raise_for_status()
                return response.json()
        except Exception:
            return None
        
auth_client = AuthServiceClient()