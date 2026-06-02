from pydantic import BaseModel, field_validator, ConfigDict
from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv


from ordner.model_ordner import DBOrdner
from ordner.base import BaseAPI



router = APIRouter(prefix="/ordner", tags=["Ordner"])

class Ordner_erstellen(BaseModel):
    title: str



    @field_validator('title')
    @classmethod
    def ueberpruefen_ob_ordner_keinen__hat(cls, value: str):
        if not value.strip(): # entfernt die leerzeichen am anfang und am ende des namens.  Wenn kein Name eingegeben worden ist, dann wirft es einen Fehler.
            raise ValueError('Bitte vergebe deinem Ordner einen Namen.')
        return value


class Ordner_Response(BaseModel):
    ordnerid: int
    title: str

    model_config = ConfigDict(from_attributes=True) # Greift auf die Daten der DB zu.
@cbv(router)
class Ordner_API(BaseAPI):
    @router.get("/", response_model=list[Ordner_Response])
    def alle_ordner_erhalten(self):
        return self.db.query(DBOrdner).all()

    @router.get("/{ordner_id}", response_model=Ordner_Response)
    def ordner_anhand_id_erhalten(self, ordner_id: int):
        return self.get_or_404(DBOrdner, ordner_id, "ordnerid")

    @router.post("/", response_model=Ordner_Response)
    def ordner_erstellen(self, ordner: Ordner_erstellen):
        db_ordner = DBOrdner(title=ordner.title)
        self.db.add(db_ordner)
        self.db.commit()
        self.db.refresh(db_ordner)
        print(self.db)
        return db_ordner


    @router.delete("/{ordner_id}")
    def ordner_entfernen(self, ordner_id: int):
        db_ordner = self.get_or_404(DBOrdner, ordner_id, "ordnerid")
        self.db.delete(db_ordner)
        self.db.commit()

    @router.put("/{ordner_id}", response_model=Ordner_Response)
    def ordner_veraendern(self, ordner_id: int, item: Ordner_erstellen):
        db_ordner = self.get_or_404(DBOrdner, ordner_id, "ordnerid")


        db_ordner.title = item.title


        self.db.add(db_ordner)
        self.db.commit()
        self.db.refresh(db_ordner)

        return db_ordner

