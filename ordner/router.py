from fastapi import APIRouter, Query
from fastapi_restful.cbv import cbv
from pydantic import BaseModel, ConfigDict, field_validator

from base import BaseAPI
from model import DBOrdner, DBUser


router = APIRouter(prefix="/ordner", tags=["Ordner"])


class OrdnerErstellen(BaseModel):
    title: str
    userid: int
    farbe: str | None = None

    @field_validator('title')
    @classmethod
    def title_pruefen(cls, value: str):
        if not value.strip():
            raise ValueError('Bitte vergebe deinem Ordner einen Namen.')
        return value


class OrdnerResponse(BaseModel):
    ordnerid: int
    title: str
    userid: int
    farbe: str | None = None

    model_config = ConfigDict(from_attributes=True)


@cbv(router)
class OrdnerAPI(BaseAPI):

# beim ordner erhalten mit Hilfe von KI Prompt: Kannst du mir beim Endpunkt alle_ordner_erhalten helfen?
    @router.get("/", response_model=list[OrdnerResponse])
    def alle_ordner_erhalten(
            self,
            aktueller_user_id: int = Query(...),
            suche: str | None = None,
            sortierung: str = "asc"
    ):
        user = self.get_or_404(DBUser, aktueller_user_id, "userid")

        query = self.db.query(DBOrdner)

        if user.rolle != "admin":
            query = query.filter(DBOrdner.userid == aktueller_user_id)

        if suche:
            query = query.filter(DBOrdner.title.contains(suche))

        if sortierung == "desc":
            query = query.order_by(DBOrdner.title.desc())
        else:
            query = query.order_by(DBOrdner.title.asc())

        return query.all()

    @router.get("/{ordner_id}", response_model=OrdnerResponse)
    def ordner_anhand_id_erhalten(self, ordner_id: int, aktueller_user_id: int = Query(...)):
        return self.check_ordner_besitzer_oder_admin(ordner_id, aktueller_user_id)

    @router.post("/", response_model=OrdnerResponse, status_code=201)
    def ordner_erstellen(self, ordner: OrdnerErstellen):
        self.get_or_404(DBUser, ordner.userid, "userid")

        db_ordner = DBOrdner(
            title=ordner.title,
            userid=ordner.userid,
            farbe=ordner.farbe
        )

        self.db.add(db_ordner)
        self.db.commit()
        self.db.refresh(db_ordner)

        return db_ordner

# mit Hilfe von KI Prompt: Hilf mir bei diesem Endpunkt weiter
    @router.put("/{ordner_id}", response_model=OrdnerResponse)
    def ordner_veraendern(
            self,
            ordner_id: int,
            item: OrdnerErstellen,
            aktueller_user_id: int = Query(...)
    ):
        db_ordner = self.check_ordner_besitzer_oder_admin(ordner_id, aktueller_user_id)

        db_ordner.title = item.title
        db_ordner.farbe = item.farbe

        self.db.commit()
        self.db.refresh(db_ordner)

        return db_ordner

    @router.delete("/{ordner_id}", status_code=200)
    def ordner_entfernen(self, ordner_id: int, aktueller_user_id: int = Query(...)):
        db_ordner = self.check_ordner_besitzer_oder_admin(ordner_id, aktueller_user_id)

        self.db.delete(db_ordner)
        self.db.commit()

        return {"message": "Ordner wurde gelöscht."}