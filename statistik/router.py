from datetime import datetime

from fastapi import APIRouter, Query
from fastapi_restful.cbv import cbv
from pydantic import BaseModel, ConfigDict
from sqlalchemy import func

from base import BaseAPI
from model import DBStatistik, DBOrdner, DBKarteikarte, DBUser

router = APIRouter(prefix="/statistik", tags=["Statistik"])


class StatistikErstellen(BaseModel):
    ordnerid: int
    richtige_antworten: int
    falsche_antworten: int


class StatistikResponse(BaseModel):
    statistikid: int
    ordnerid: int
    richtige_antworten: int
    falsche_antworten: int
    datum: datetime

    model_config = ConfigDict(from_attributes=True)


@cbv(router)
class StatistikAPI(BaseAPI):

    @router.get("/", response_model=list[StatistikResponse])
    def alle_statistiken_erhalten(self, aktueller_user_id: int = Query(...)):
        user = self.get_or_404(DBUser, aktueller_user_id, "userid")

        query = self.db.query(DBStatistik).join(DBOrdner)

        if user.rolle != "admin":
            query = query.filter(DBOrdner.userid == aktueller_user_id)

        return query.all()

    @router.post("/", response_model=StatistikResponse, status_code=201)
    def statistik_erstellen(
        self,
        statistik: StatistikErstellen,
        aktueller_user_id: int = Query(...)
    ):
        self.check_ordner_besitzer_oder_admin(statistik.ordnerid, aktueller_user_id)

        db_statistik = DBStatistik(
            ordnerid=statistik.ordnerid,
            richtige_antworten=statistik.richtige_antworten,
            falsche_antworten=statistik.falsche_antworten,
            datum=datetime.now()
        )

        self.db.add(db_statistik)
        self.db.commit()
        self.db.refresh(db_statistik)

        return db_statistik

    @router.get("/karten-pro-ordner")
    def karten_pro_ordner(self, aktueller_user_id: int = Query(...)):
        user = self.get_or_404(DBUser, aktueller_user_id, "userid")

        query = self.db.query(
            DBOrdner.ordnerid,
            DBOrdner.title,
            func.count(DBKarteikarte.karteikartenid).label("anzahl_karteikarten")
        ).outerjoin(DBKarteikarte).group_by(DBOrdner.ordnerid)

        if user.rolle != "admin":
            query = query.filter(DBOrdner.userid == aktueller_user_id)

        ergebnis = query.all()

        return [
            {
                "ordnerid": item.ordnerid,
                "ordner": item.title,
                "anzahl_karteikarten": item.anzahl_karteikarten
            }
            for item in ergebnis
        ]

    @router.get("/quiz-auswertung/{ordner_id}")
    def quiz_auswertung(self, ordner_id: int, aktueller_user_id: int = Query(...)):
        self.check_ordner_besitzer_oder_admin(ordner_id, aktueller_user_id)

        richtige = self.db.query(func.sum(DBStatistik.richtige_antworten)).filter(
            DBStatistik.ordnerid == ordner_id
        ).scalar()

        falsche = self.db.query(func.sum(DBStatistik.falsche_antworten)).filter(
            DBStatistik.ordnerid == ordner_id
        ).scalar()

        richtige = richtige or 0
        falsche = falsche or 0
        gesamt = richtige + falsche

        if gesamt == 0:
            prozent = 0
        else:
            prozent = round((richtige / gesamt) * 100, 2)

        return {
            "ordnerid": ordner_id,
            "richtige_antworten": richtige,
            "falsche_antworten": falsche,
            "gesamt": gesamt,
            "erfolgsquote_prozent": prozent
        }