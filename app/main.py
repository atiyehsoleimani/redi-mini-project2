from fastapi import FastAPI
from app.routes import routes

app = FastAPI(title="Tasks Manager")

app.include_router(routes.router)
