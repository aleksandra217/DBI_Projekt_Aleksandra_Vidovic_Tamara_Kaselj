from fastapi import APIRouter, Query
from fastapi_restful.cbv import cbv
from pydantic import BaseModel, ConfigDict, field_validator

from base import BaseAPI
from model import DBKarteikarte, DBOrdner, DBUser

router = APIRouter(prefix="/karteikarten", tags=["Karteikarten"])


class KarteikarteErstellen(BaseModel):
    typ: str
    text_frage: str
    text_loesung: str
    ordnerid: int

    @field_validator("typ")
    @classmethod
    def typ_pruefen(cls, value: str):
        erlaubte_typen = ["offen", "truefalse", "multiplechoice"]

        if value not in erlaubte_typen:
            raise ValueError("Typ muss offen, truefalse oder multiplechoice sein.")

        return value

    @field_validator("text_frage")
    @classmethod
    def frage_pruefen(cls, value: str):
        if not value.strip():
            raise ValueError("Die Frage darf nicht leer sein.")
        return value


class KarteikarteResponse(BaseModel):
    karteikartenid: int
    typ: str
    text_frage: str
    text_loesung: str
    ordnerid: int

    model_config = ConfigDict(from_attributes=True)


class KarteikarteMitOrdnerResponse(BaseModel):
    karteikartenid: int
    typ: str
    text_frage: str
    text_loesung: str
    ordner_title: str


@cbv(router)
class KarteikartenAPI(BaseAPI):

    @router.get("/", response_model=list[KarteikarteResponse])
    def alle_karteikarten_erhalten(
        self,
        aktueller_user_id: int = Query(...),
        ordnerid: int | None = None,
        typ: str | None = None,
        suche: str | None = None,
        sortierung: str = "asc"
    ):
        query = self.db.query(DBKarteikarte).join(DBOrdner)

        user = self.get_or_404(DBUser, aktueller_user_id, "userid")

        if user.rolle != "admin":
            query = query.filter(DBOrdner.userid == aktueller_user_id)

        if ordnerid is not None:
            query = query.filter(DBKarteikarte.ordnerid == ordnerid)

        if typ is not None:
            query = query.filter(DBKarteikarte.typ == typ)

        if suche:
            query = query.filter(DBKarteikarte.text_frage.contains(suche))

        if sortierung == "desc":
            query = query.order_by(DBKarteikarte.karteikartenid.desc())
        else:
            query = query.order_by(DBKarteikarte.karteikartenid.asc())

        return query.all()

    @router.get("/mit-ordner", response_model=list[KarteikarteMitOrdnerResponse])
    def karteikarten_mit_ordner_join(self, aktueller_user_id: int = Query(...)):
        user = self.get_or_404(DBUser, aktueller_user_id, "userid")

        query = self.db.query(
            DBKarteikarte.karteikartenid,
            DBKarteikarte.typ,
            DBKarteikarte.text_frage,
            DBKarteikarte.text_loesung,
            DBOrdner.title.label("ordner_title")
        ).join(DBOrdner)

        if user.rolle != "admin":
            query = query.filter(DBOrdner.userid == aktueller_user_id)

        ergebnis = query.all()

        return [
            {
                "karteikartenid": item.karteikartenid,
                "typ": item.typ,
                "text_frage": item.text_frage,
                "text_loesung": item.text_loesung,
                "ordner_title": item.ordner_title
            }
            for item in ergebnis
        ]

    @router.get("/{karteikarten_id}", response_model=KarteikarteResponse)
    def karteikarte_anhand_id_erhalten(
        self,
        karteikarten_id: int,
        aktueller_user_id: int = Query(...)
    ):
        karte = self.get_or_404(DBKarteikarte, karteikarten_id, "karteikartenid")
        self.check_ordner_besitzer_oder_admin(karte.ordnerid, aktueller_user_id)

        return karte

    @router.post("/", response_model=KarteikarteResponse, status_code=201)
    def karteikarte_erstellen(
        self,
        karteikarte: KarteikarteErstellen,
        aktueller_user_id: int = Query(...)
    ):
        self.check_ordner_besitzer_oder_admin(karteikarte.ordnerid, aktueller_user_id)

        db_karte = DBKarteikarte(
            typ=karteikarte.typ,
            text_frage=karteikarte.text_frage,
            text_loesung=karteikarte.text_loesung,
            ordnerid=karteikarte.ordnerid
        )

        self.db.add(db_karte)
        self.db.commit()
        self.db.refresh(db_karte)

        return db_karte

    @router.put("/{karteikarten_id}", response_model=KarteikarteResponse)
    def karteikarte_veraendern(
        self,
        karteikarten_id: int,
        item: KarteikarteErstellen,
        aktueller_user_id: int = Query(...)
    ):
        db_karte = self.get_or_404(DBKarteikarte, karteikarten_id, "karteikartenid")
        self.check_ordner_besitzer_oder_admin(db_karte.ordnerid, aktueller_user_id)

        db_karte.typ = item.typ
        db_karte.text_frage = item.text_frage
        db_karte.text_loesung = item.text_loesung

        self.db.commit()
        self.db.refresh(db_karte)

        return db_karte

    @router.delete("/{karteikarten_id}")
    def karteikarte_entfernen(
        self,
        karteikarten_id: int,
        aktueller_user_id: int = Query(...)
    ):
        db_karte = self.get_or_404(DBKarteikarte, karteikarten_id, "karteikartenid")
        self.check_ordner_besitzer_oder_admin(db_karte.ordnerid, aktueller_user_id)

        self.db.delete(db_karte)
        self.db.commit()

        return {"message": "Karteikarte wurde gelöscht."}