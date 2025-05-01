from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import user_routes, chat_routes, chat_ws

# from db.database import engine, Base
# print(">>> Creating tables...")
# Base.metadata.create_all(bind=engine)
# print(">>> Tables created.")

app = FastAPI(
    title="Messenger API",
    description="Мессенджер",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_ws.router)
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(chat_routes.router, prefix="/chats", tags=["Сhats"])
