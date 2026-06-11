import uvicorn
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette import status

from database import Base, engine
from logger_config import logger

from users.router import router as user_router
from ordner.router import router as ordner_router
from karteikarten.router import router as karteikarten_router
from quiz.router import router as quiz_router
from statistik.router import router as statistik_router




Base.metadata.create_all(bind=engine)
app = FastAPI(title="Karteikartensystem", description="Karteikartensystem", version="1.0.0")

@app.middleware("http")
async def log_request(request: Request, call_next):
    start_time = time.time()

    logger.info(f"Request gestartet: {request.method} {request.url.path}")

    try:
        response = await call_next(request)

        dauer = round(time.time() - start_time, 4)

        logger.info(
            f"Request beendet: {request.method} {request.url.path} "
            f"Statuscode: {response.status_code} Dauer: {dauer}s"
        )

        return response

    except Exception as fehler:
        dauer = round(time.time() - start_time, 4)

        logger.error(
            f"Fehler bei Request: {request.method} {request.url.path} "
            f"Dauer: {dauer}s Fehler: {str(fehler)}")

        return JSONResponse(status_code=500, content={"detail": "Interner Serverfehler. Bitte überprüfen die Logs."})



app.include_router(user_router)
app.include_router(ordner_router)
app.include_router(karteikarten_router)
app.include_router(quiz_router)
app.include_router(statistik_router)


@app.get("/") 
def root():
    logger.info("Root-Endpunkte wurden aufgerufen.")
    return {"message": "Unser Karteikartensystem."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=1024)