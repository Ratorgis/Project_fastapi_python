from fastapi import FastAPI, Response, HTTPException, status
from pydantic import BaseModel

from service.link_service import LinkService

class LinkRequest(BaseModel):
    link : str

class LinkResponse(BaseModel):
    short_link : str

def create_app() -> FastAPI:
    app = FastAPI()
    link_service = LinkService()

    @app.post("/link")
    def create_link(payload: LinkRequest) -> LinkResponse:
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
