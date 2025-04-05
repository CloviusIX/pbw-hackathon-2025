from fastapi import FastAPI

from xrpl_backend_2025.api import include_routes

app = FastAPI()

include_routes(app)
