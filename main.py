import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
from src.api import api_router
from src.controller.UserController import load_default_admin_user


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])
app.include_router(api_router)
#load_default_admin_user(app, db)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
