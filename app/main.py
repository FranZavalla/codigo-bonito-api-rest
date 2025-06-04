from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.layer_0_db_definition.database_ponyorm import init_pony
from app.layer_0_db_definition.database_sqlalchemy import init_sqlalchemy
from app.layer_3_api.products import router as products_router
from app.layer_3_api.products_with_usd_prices import \
    router as products_with_usd_prices_router
from app.settings import settings


def init_db():
    print("Initializing database...")
    if settings.ORM == "sqlalchemy":
        init_sqlalchemy()
    else:
        init_pony()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    pass


app = FastAPI(lifespan=lifespan)

app.include_router(products_router, prefix="/products", tags=["products"])
app.include_router(
    products_with_usd_prices_router,
    prefix="/products_with_usd_prices",
    tags=["products"],
)


@app.get("/")
def health_check():
    return JSONResponse(status_code=200, content={"detail": "Healthy"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
