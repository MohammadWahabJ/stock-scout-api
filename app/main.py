from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, stock
from app.db import models
from app.db.session import engine
from app.utils import verify_access_token
from sqlalchemy.orm import sessionmaker
from fastapi import Request
from fastapi.responses import JSONResponse

# Create the FastAPI application instance
app = FastAPI(
    title="FastAPI Stock Dashboard",
    description="A simple FastAPI application for stock management and authentication.",
    version="1.0.0",
)

# Database setup
models.Base.metadata.create_all(bind=engine)

# Set up CORS (allow requests from frontend)
origins = [
    "http://localhost:3000",  # if your frontend is running on port 3000
    "http://localhost:8000",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["GET"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include the authentication and stock routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(stock.router, prefix="/stocks", tags=["stocks"])

# JWT Middleware for token validation (if needed)


@app.middleware("http")
async def add_jwt_validation(request: Request, call_next):
    # Skip authentication for public routes
    if request.url.path in ["/", "/auth", "/auth/register", "/auth/login", "/auth/token", "/docs", "/openapi.json"]:
        response = await call_next(request)
        return response

    # Extract the token from headers (if any)
    token = request.cookies.get(
        "access_token") or request.headers.get("Authorization")

    if token:
        # Verify JWT token
        try:
            payload = verify_access_token(token)
            request.state.user = payload  # Attach user info to the request state
        except Exception as e:
            return JSONResponse(content={"detail": "Unauthorized"}, status_code=401)

    else:
        return JSONResponse(content={"detail": "Unauthorized"}, status_code=401)

    # Proceed with the request
    response = await call_next(request)
    return response

# Root endpoint (for testing)


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Stock Dashboard!"}
