from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.api.api_v1.endpoints import applications, enrollees, employees, specialities

api_router = APIRouter()
api_router.include_router(
    applications.router, prefix="/applications", tags=["applications"]
)
api_router.include_router(enrollees.router, prefix="/enrollees", tags=["enrollees"])
api_router.include_router(employees.router, prefix="/employees", tags=["employees"])
api_router.include_router(
    specialities.router, prefix="/specialities", tags=["specialities"]
)

templates = Jinja2Templates(directory="templates")


@api_router.get("/")
def read_main(request: Request):
    return templates.TemplateResponse(request=request, name="base_admin.html")
