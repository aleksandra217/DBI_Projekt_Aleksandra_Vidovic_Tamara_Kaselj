from datetime import date, datetime

from pydantic import BaseModel, field_validator, ConfigDict
from fastapi import APIRouter
from fastapi_restful.cbv import cbv


from model import DBStatistik
from users.base import BaseAPI
from typing import Optional, Any




router = APIRouter(prefix="/statistik", tags=["Statistik"])

class Statistik_erstellen(BaseModel):
    ordnerid: int
    richtige_antworten: int
    falsche_antworten: int
    # Wieso bekomme ich einen 500 Internal Server Error? Lösung: statt datetime setzen, ein Optional[Any] = None setzen, weil falls es momentan keine Daten liefert, dann stürtzt das Programm nicht ab und man bekommt trotzdem seinen aktuellen stand.
    #aktualisierungsstatistik: Optional[Any] = None


class Statistik_Response(Statistik_erstellen):
    statistikid: int
    ordnerid: int
    richtige_antworten: int
    falsche_antworten: int
    datum: datetime


    model_config = ConfigDict(from_attributes=True) # Greift auf die Daten von der DB zu.
@cbv(router)
class Statistik_API(BaseAPI):
 # vielleicht alle anzeigen lassen?

    @router.get("/{statistik_id}", response_model=Statistik_Response)
    def statistik_anhand_id_erhalten(self, statistik_id: int):
        return self.get_or_404(DBStatistik, statistik_id, "statistikid")

    @router.post("/", response_model=Statistik_Response)
    def statistik_erstellen(self, statistik: Statistik_erstellen):
        db_statistik = DBStatistik(ordnerid=statistik.ordnerid,richtige_antworten=statistik.richtige_antworten, falsche_antworten=statistik.falsche_antworten)
        self.db.add(db_statistik)
        self.db.commit()
        self.db.refresh(db_statistik)
        print(self.db)
        return db_statistik


    @router.delete("/{statistik_id}")
    def statistik_entfernen(self, statistik_id: int):
        db_statistik = self.get_or_404(DBStatistik, statistik_id, "statistikid")
        self.db.delete(db_statistik)
        self.db.commit()

    @router.put("/{statistik_id}", response_model=Statistik_Response)
    def Statistik_veraendern(self, statistik_id: int, item: Statistik_erstellen):
        db_statistik = self.get_or_404(DBStatistik, statistik_id, "statistikid")

        db_statistik.ordnerid = item.ordnerid
        db_statistik.richtige_antworten = item.richtige_antworten
        db_statistik.falsche_antworten = item.falsche_antworten
        self.db.add(db_statistik)
        self.db.commit()
        self.db.refresh(db_statistik)

        return db_statistik
