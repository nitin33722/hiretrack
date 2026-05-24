import uuid
import time
import logging
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import httpx
from app.core.config import settings


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


limiter = Limiter(key_func=get_remote_address)


app = FastAPI(
    title="HireTrack API Gateway",
    description="Single entry point for all HireTrack services",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # React dev server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


ROUTING_TABLE = {
    "/auth": settings.AUTH_SERVICE_URL,
    "/jobs": settings.JOB_SERVICE_URL,
    "/applications": settings.APPLICATION_SERVICE_URL,
    "/files": settings.FILE_SERVICE_URL,
    "/health": None,  # Handled locally
}

def get_target_url(path: str) -> str:
    for prefix, service_url in ROUTING_TABLE.items():
        if path.startswith(prefix) and service_url:
            return f"{service_url}{path}"
    return None

@app.get("/health")
async def health_check():
    """Gateway health check"""
    return {
        "status": "healthy",
        "service": "api-gateway",
        "version": "1.0.0"
    }

@app.get("/health/all")
async def health_check_all():
    services = {
        "auth-service": f"{settings.AUTH_SERVICE_URL}/health",
        "job-service": f"{settings.JOB_SERVICE_URL}/health",
        "application-service": f"{settings.APPLICATION_SERVICE_URL}/health",
        "file-service": f"{settings.FILE_SERVICE_URL}/health",
    }
    
    results = {}
    
    async with httpx.AsyncClient(timeout=3.0) as client:
        for service_name, health_url in services.items():
            try:
                response = await client.get(health_url)
                results[service_name] = response.json()
            except Exception as e:
                results[service_name] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
    
    all_healthy = all(
        r.get("status") == "healthy"
        for r in results.values()
    )
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "gateway": "healthy",
        "services": results
    }

@app.api_route(
    "/{full_path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"]
)
@limiter.limit(settings.RATE_LIMIT)
async def proxy(request: Request, full_path: str):
    request_id = str(uuid.uuid4())[:8]
    
    start_time = time.time()
    logger.info(
        f"[{request_id}] {request.method} /{full_path} "
        f"from {request.client.host}"
    )
    
    path = f"/{full_path}"
    target_url = get_target_url(path)
    
    if not target_url:
        raise HTTPException(
            status_code=404,
            detail=f"No service found for path: {path}"
        )
    
    headers = dict(request.headers)
    
    headers["X-Request-ID"] = request_id
    
    headers.pop("host", None)
    headers.pop("content-length", None)
    
    query_params = dict(request.query_params)
    
    body = await request.body()
    
    content_type = request.headers.get("content-type", "")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            if "multipart/form-data" in content_type:
                # For file uploads, read form data and forward as multipart
                form_data = await request.form()
                files = {}
                data = {}
                
                for key, value in form_data.items():
                    if hasattr(value, "read"):
                        # It's a file
                        file_bytes = await value.read()
                        files[key] = (value.filename, file_bytes, value.content_type)
                    else:
                        # It's a regular form field
                        data[key] = value
                
                response = await client.request(
                    method=request.method,
                    url=target_url,
                    headers={k: v for k, v in headers.items() if "content-type" not in k},
                    params=query_params,
                    files=files if files else None,
                    data=data if data else None,
                )
            else:
                # For JSON and other requests
                response = await client.request(
                    method=request.method,
                    url=target_url,
                    headers=headers,
                    params=query_params,
                    content=body,
                )
        
        # Step 5: Log response
        duration = (time.time() - start_time) * 1000
        logger.info(
            f"[{request_id}] {response.status_code} "
            f"in {duration:.1f}ms → {target_url}"
        )
        
        # Step 6: Return response to client
        response_headers = dict(response.headers)
        response_headers.pop("content-encoding", None)
        response_headers.pop("transfer-encoding", None)
        
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=response_headers,
            media_type=response.headers.get("content-type")
        )
    
    except httpx.TimeoutException:
        logger.error(f"[{request_id}] Timeout calling {target_url}")
        raise HTTPException(
            status_code=503,
            detail=f"Service timeout: {target_url}"
        )
    except httpx.ConnectError:
        logger.error(f"[{request_id}] Connection failed to {target_url}")
        raise HTTPException(
            status_code=503,
            detail="Service unavailable"
        )
    