from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.dependencies_container import DependenciesContainer

API_V1_PREFIX = "/v1"


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    container = DependenciesContainer()
    await container.initialize()
    fastapi_app.state.container = container

    auth_handler = container.get_auth_handler()
    user_handler = container.get_user_handler()

    fastapi_app.include_router(auth_handler.router, prefix=API_V1_PREFIX)
    fastapi_app.include_router(user_handler.router, prefix=API_V1_PREFIX)

    yield

    await container.close()


app = FastAPI(title="Auth Service", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "auth-service"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
