import time
import logging
from fastapi import Request
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger("api")

async def log_request_middleware(request: Request, call_next):
    """
    Middleware to log all requests and responses
    """
    request_id = str(time.time())
    
    # Log request
    logger.info(f"Request {request_id} - {request.method} {request.url.path}")
    
    # Log request body for non-GET requests
    if request.method != "GET":
        try:
            body = await request.body()
            if body:
                logger.info(f"Request {request_id} body: {body.decode()}")
        except Exception as e:
            logger.error(f"Error parsing request body: {e}")
    
    # Process the request
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Log response
    logger.info(f"Response {request_id} - Status: {response.status_code} - Time: {process_time:.3f}s")
    
    return response 