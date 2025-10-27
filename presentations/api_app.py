import time
from fastapi import FastAPI, Request, Response, HTTPException, status
from pydantic import BaseModel
from loguru import logger

from utils.strings import link_valid, auto_complete_link
from service.link_service import LinkService

class LinkRequest(BaseModel):
    link : str

class LinkResponse(BaseModel):
    short_link : str

def create_app() -> FastAPI:
    app = FastAPI()
    link_service = LinkService()

    @app.middleware('http')
    async def add_process_time_header(request: Request, call_next) -> Response:
        try:
            t0 = time.time()
            response: Response = await call_next(request)
            elapse_ms = round((time.time() - t0) * 1000, 2)
            response.headers["X-Latency"] = f"{elapse_ms} ms"
            return response
        except Exception:
            logger.exception("failed to read body")
            return Response(status_code = status.HTTP_400_BAD_REQUEST)
    @app.post("/link")
    def create_link(payload: LinkRequest) -> LinkResponse:
        payload.link = auto_complete_link(payload.link)
        if not link_valid(payload.link):
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail = 'not valid link to request'
            )
        short_link = link_service.create_link(payload.link)

        return LinkResponse(short_link = f'http://localhost:8000/{short_link}')
        
    @app.get("/{link}")
    def get_link(link: str) -> Response:
        long_link = link_service.get_link(link)
        if long_link is None:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND, 
                detail = "link not found"
            )

        return Response(
            status_code = status.HTTP_301_MOVED_PERMANENTLY, 
            headers={"Location": long_link}
        )

    return app 


