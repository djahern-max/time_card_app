from fastapi import FastAPI
from .routers import auth, timecards
from .database import engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(timecards.router)