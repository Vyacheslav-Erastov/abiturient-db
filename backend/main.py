from fastapi import Depends, FastAPI, Form, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.api.api_v1.api import api_router
from app.core.config import settings
from starlette.middleware.cors import CORSMiddleware
# from security import AuthHandler
from app import schemas, crud, models
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="templates")
# auth_handler = AuthHandler()

app.include_router(api_router, prefix=settings.API_V1_STR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.middleware("http")
# def create_auth_header(
#     request: Request,
#     call_next,
# ):
#     """
#     Check if there are cookies set for authorization. If so, construct the
#     Authorization header and modify the request (unless the header already
#     exists!)
#     """
#     if "Authorization" not in request.headers and "Authorization" in request.cookies:
#         access_token = request.cookies["Authorization"]

#         request.headers.__dict__["_list"].append(
#             (
#                 "authorization".encode(),
#                 f"Bearer {access_token}".encode(),
#             )
#         )
#     elif (
#         "Authorization" not in request.headers
#         and "Authorization" not in request.cookies
#     ):
#         request.headers.__dict__["_list"].append(
#             (
#                 "authorization".encode(),
#                 f"Bearer 12345".encode(),
#             )
#         )
#     response = call_next(request)
#     return response


if "__main__" == __name__:
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
