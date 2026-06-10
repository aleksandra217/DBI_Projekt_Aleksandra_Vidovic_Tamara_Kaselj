from fastapi import APIRouter
from fastapi_restful.cbv import cbv
from pydantic import BaseModel, ConfigDict

from karteikarten.base import BaseAPI
from model import DBKarteikarten

router = APIRouter(prefix="/karteikarten", tags=["Karteikarten"])

class Karteikarten_erstellen(BaseModel):
    text_frage: str
    text_loesung: str
    ordnerid: int



class Karteikarten_Response(BaseModel):
    karteikartenid: int
    text_frage: str
    text_loesung: str

    model_config = ConfigDict(from_attributes=True) # Greift auf die Daten der DB zu.
@cbv(router)
class Karteikarten_API(BaseAPI):
    @router.get("/", response_model=list[Karteikarten_Response])
    def alle_karteikarten_erhalten(self):
        return self.db.query(DBKarteikarten).all()

    @router.get("/{karteikarten_id}", response_model=Karteikarten_Response)
    def karteikarten_anhand_id_erhalten(self, karteikarten_id: int):
        return self.get_or_404(DBKarteikarten, karteikarten_id, "karteikartenid")

    @router.get("/ordner/{ordner_id}", response_model=list[Karteikarten_Response])
    def karteikarten_eines_ordners_erhalten(self, ordner_id: int):
        return self.db.query(DBKarteikarten).filter(DBKarteikarten.ordnerid == ordner_id).all()


    @router.post("/", response_model=Karteikarten_Response)
    def karteikarten_erstellen(self, karteikarten: Karteikarten_erstellen):
        db_karteikarten = DBKarteikarten(text_frage=karteikarten.text_frage, text_loesung=karteikarten.text_loesung, ordnerid=karteikarten.ordnerid)
        self.db.add(db_karteikarten)
        self.db.commit()
        self.db.refresh(db_karteikarten)
        print(self.db)
        return db_karteikarten


    @router.delete("/{karteikarten_id}")
    def karteikarten_entfernen(self, karteikarten_id: int):
        db_karteikarten = self.get_or_404(DBKarteikarten, karteikarten_id, "karteikartenid")
        self.db.delete(db_karteikarten)
        self.db.commit()

    @router.put("/{karteikarten_id}", response_model=Karteikarten_Response)
    def karteikarten_veraendern(self, karteikarten_id: int, item: Karteikarten_erstellen):
        db_karteikarten = self.get_or_404(DBKarteikarten, karteikarten_id, "karteikartenid")


        db_karteikarten.text_frage = item.text_frage
        db_karteikarten.text_loesung = item.text_loesung


        self.db.add(db_karteikarten)
        self.db.commit()
        self.db.refresh(db_karteikarten)

        return db_karteikarten

