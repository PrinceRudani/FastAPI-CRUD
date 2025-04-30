from fastapi import Request, HTTPException, status
from base.utils.constant import constant


async def verify_api_key(request: Request):
    api_key = request.headers.get("X-API-Key")
    if api_key != constant.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
