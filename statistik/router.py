from datetime import datetime

from pydantic import BaseModel, field_validator, ConfigDict
from fastapi import APIRouter
from fastapi_restful.cbv import cbv


from users.model import DBUser
from users.base import BaseAPI




router = APIRouter(prefix="/statistik", tags=["Statistik"])

class Statistik_erstellen(BaseModel):
    richtige_antworten: int
    falsche_antworten: int
    aktualisierungsStatistik: datetime


class Statistik_Response(Statistik_erstellen):
    statistikid: int
    richtige_antworten: int
    falsche_antworten: int


    model_config = ConfigDict(from_attributes=True) # Greift auf die Daten von der DB zu.
@cbv(router)
class Statistik_API(BaseAPI):
 # vielleicht alle anzeigen lassen?

    @router.get("/{statistik_id}", response_model=Statistik_Response)
    def statistik_anhand_id_erhalten(self, statistik_id: int):
        return self.get_or_404(DBStatistik, statistik_id, "statistikid")

    @router.post("/", response_model=Statistik_Response)
    def user_erstellen(self, user: Statistik_erstellen):
        db_statistik = DBStatistik(richtige_antworten=statistik.richtige_antworten, falsche_antworten=statistik.falsche_antworten)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        print(self.db)
        return db_user


    @router.delete("/{user_id}")
    def user_entfernen(self, user_id: int):
        db_user = self.get_or_404(DBUser, user_id, "userid")
        self.db.delete(db_user)
        self.db.commit()

    @router.put("/{user_id}", response_model=User_Response)
    def user_veraendern(self, user_id: int, item: User_erstellen):
        db_user = self.get_or_404(DBUser, user_id, "userid")

        db_user.name = item.name
        db_user.email_adresse = item.email_adresse

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

