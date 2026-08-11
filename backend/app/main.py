from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.db.driver import close_driver
from app.errors import DatabaseUnavailableError, NotFoundError
from app.routers import health, people, projects, skills, staffing

settings = get_settings()

app = FastAPI(title="Staffing Graph API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(people.router)
app.include_router(projects.router)
app.include_router(skills.router)
app.include_router(staffing.router)


@app.exception_handler(DatabaseUnavailableError)
def database_unavailable_handler(request: Request, exc: DatabaseUnavailableError):
    return JSONResponse(
        status_code=503,
        content={"error": "database_unavailable", "message": str(exc)},
    )


@app.exception_handler(NotFoundError)
def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"error": "not_found", "message": exc.message},
    )


@app.on_event("shutdown")
def shutdown():
    close_driver()
