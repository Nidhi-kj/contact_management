
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import user as user_router
from routers import contacts as contact_router
from routers import company as company_router
from routers import phone as phone_router
from routers import notes as notes_router

from main.database import Base, engine

# Models import karna zaroori hai
from models import user, contacts, notes, company, phone

# Database tables create karna
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers connect karna
app.include_router(user_router.router)
app.include_router(contact_router.router)
app.include_router(company_router.router)
app.include_router(phone_router.router)
app.include_router(notes_router.router)


@app.get("/")
def home():
    return {"message": "Contact Management System"}






# from fastapi import FastAPI
# from routers import user as user_router
# from routers import contacts as contact_router
# from routers import company as company_router
# from routers import phone as phone_router
# from routers import notes as notes_router

# from main.database import Base, engine
# # Models import karna zaroori hai
# from models import user, contacts, notes, company, phone

# # Tables create karna
# Base.metadata.create_all(bind=engine)

# app = FastAPI()
# # Router connect
# app.include_router(user_router.router)
# # app.include_router(contacts_router.router)
# app.include_router(contact_router.router)
# app.include_router(company_router.router)
# app.include_router(phone_router.router)
# app.include_router(notes_router.router)
# @app.get("/")
# def home():
#     return {"message": "Contact Management System"}