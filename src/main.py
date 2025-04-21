from fastapi import FastAPI, Depends
from settings import settings
from layer_0_db_definition.database_ponyorm import init_pony
from layer_0_db_definition.database_sqlalchemy import init_sqlalchemy


def init_db():
    print("Initializing database...")
    if settings.ORM == "sqlalchemy":
        init_sqlalchemy()
    else:
        init_pony()


app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def health_check():
    return {"message": "Healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
