from fastapi import FastAPI
from app.routes import routes
from fastapi.staticfiles import StaticFiles
from app.routes import pages

app = FastAPI(title="Tasks Manager")

app.include_router(routes.router)

app.include_router(pages.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static") 

