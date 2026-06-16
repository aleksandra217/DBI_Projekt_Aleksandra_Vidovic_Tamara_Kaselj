from fastapi import APIRouter, Query, HTTPException
from fastapi_restful.cbv import cbv
from pydantic import BaseModel, ConfigDict

from base import BaseAPI
from model import DBQuiz, DBKarteikarte, DBQuizKarteikarte, DBOrdner, DBUser

router = APIRouter(prefix="/quiz", tags=["Quiz"])


class QuizErstellen(BaseModel):
    title: str
    ordnerid: int


class QuizResponse(BaseModel):
    quizid: int
    title: str
    ordnerid: int

    model_config = ConfigDict(from_attributes=True)


@cbv(router)
class QuizAPI(BaseAPI):

    @router.get("/", response_model=list[QuizResponse])
    def alle_quizzes_erhalten(self, aktueller_user_id: int = Query(...)):
        user = self.get_or_404(DBUser, aktueller_user_id, "userid")

        query = self.db.query(DBQuiz)

        if user.rolle != "admin":
            query = query.join(DBOrdner).filter(DBOrdner.userid == aktueller_user_id)

        return query.all()

    @router.get("/{quiz_id}", response_model=QuizResponse)
    def quiz_anhand_id_erhalten(self, quiz_id: int, aktueller_user_id: int = Query(...)):
        quiz = self.get_or_404(DBQuiz, quiz_id, "quizid")
        self.check_ordner_besitzer_oder_admin(quiz.ordnerid, aktueller_user_id)

        return quiz

    @router.post("/", response_model=QuizResponse, status_code=201)
    def quiz_erstellen(self, quiz: QuizErstellen, aktueller_user_id: int = Query(...)):
        self.check_ordner_besitzer_oder_admin(quiz.ordnerid, aktueller_user_id)

        db_quiz = DBQuiz(
            title=quiz.title,
            ordnerid=quiz.ordnerid
        )

        self.db.add(db_quiz)
        self.db.commit()
        self.db.refresh(db_quiz)

        return db_quiz

    @router.post("/ordner/{ordner_id}/generate", response_model=QuizResponse)
    def quiz_aus_karteikarten_erstellen(
        self,
        ordner_id: int,
        aktueller_user_id: int = Query(...),
        title: str = Query("Hallo")
    ):
        self.check_ordner_besitzer_oder_admin(ordner_id, aktueller_user_id)

        karteikarten = self.db.query(DBKarteikarte).filter(
            DBKarteikarte.ordnerid == ordner_id
        ).all()

        if len(karteikarten) == 0:
            raise HTTPException(
                status_code=400,
                detail="In diesem Ordner gibt es noch keine Karteikarten."
            )

        db_quiz = DBQuiz(
            title=title,
            ordnerid=ordner_id
        )

        self.db.add(db_quiz)
        self.db.commit()
        self.db.refresh(db_quiz)

        for karte in karteikarten:
            verbindung = DBQuizKarteikarte(
                quizid=db_quiz.quizid,
                karteikartenid=karte.karteikartenid
            )
            self.db.add(verbindung)

        self.db.commit()

        return db_quiz

    @router.get("/{quiz_id}/karteikarten")
    def quiz_karteikarten_anzeigen(self, quiz_id: int, aktueller_user_id: int = Query(...)):
        quiz = self.get_or_404(DBQuiz, quiz_id, "quizid")
        self.check_ordner_besitzer_oder_admin(quiz.ordnerid, aktueller_user_id)


        ergebnis = self.db.query(DBKarteikarte).join(DBQuizKarteikarte).filter(
            DBQuizKarteikarte.quizid == quiz_id
        ).all()

        return ergebnis

    @router.delete("/{quiz_id}")
    def quiz_entfernen(self, quiz_id: int, aktueller_user_id: int = Query(...)):
        quiz = self.get_or_404(DBQuiz, quiz_id, "quizid")
        self.check_ordner_besitzer_oder_admin(quiz.ordnerid, aktueller_user_id)

        self.db.delete(quiz)
        self.db.commit()

        return {"message": "Quiz wurde gelöscht."}