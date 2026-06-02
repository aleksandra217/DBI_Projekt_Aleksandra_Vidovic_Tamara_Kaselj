import uvicorn
from fastapi import FastAPI
from database import Base, engine
from users.router import router as user_router
from ordner.router import router as ordner_router

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Karteikartensystem", description="Karteikartensystem", version="1.0.0")

app.include_router(user_router)
app.include_router(ordner_router)


@app.get("/")
def root():
    return {"message": "Unser Karteikartensystem."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=1024)