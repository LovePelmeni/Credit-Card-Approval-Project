from fastapi.middleware.cors import CORSMiddleware
from .settings import application 
import os 

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*")

cors_middleware = CORSMiddleware(
    allow_credentials=True,
    allow_headers="*",
    allow_methods=["GET", "POST"],
    allow_origins=ALLOWED_HOSTS,
)

application.add_middleware(
    middleware_class=cors_middleware
)