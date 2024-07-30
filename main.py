import uvicorn

from fastapi import FastAPI

from core.settings import settings

from api_v1 import router as router_v1


app = FastAPI()

app.add_middleware(**settings.middleware.middleware)

app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


@app.get("/")
async def start_test():
    return {"message": "1, 2, 3 Start!"}


if __name__ == "__main__":
    uvicorn.run(
        app=settings.app,
        host=settings.host,
        port=settings.port,
        reload=settings.reload_flag,
    )
