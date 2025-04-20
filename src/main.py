from fastapi import FastAPI, Depends
from layer_3_api.products import router as products_router
from layer_3_api.products_with_usd_prices import (
    router as products_with_usd_prices_router,
)


init_pony()
app = FastAPI()

app.include_router(products_router, prefix="/products", tags=["products"])
app.include_router(
    products_with_usd_prices_router,
    prefix="/products_with_usd_prices",
    tags=["products_with_usd_prices"],
)


@app.get("/")
def health_check():
    return {"message": "Healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
