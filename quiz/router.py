from pydantic import BaseModel, field_validator, ConfigDict
from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv


from model import DBQuiz
from quiz.base import BaseAPI
from model import DBKarteikarte



router = APIRouter(prefix="/quiz", tags=["Quiz"])

class Quiz_erstellen(BaseModel):
    title: str
    ordnerid: int



class Quiz_Response(BaseModel):
    quizid: int
    title: str
    ordnerid: int

    model_config = ConfigDict(from_attributes=True) # Greift auf die Daten der DB zu.
@cbv(router)
class Quiz_API(BaseAPI):
 # alle quizzess erhalten?

    @router.get("/{quiz_id}", response_model=Quiz_Response)
    def quiz_anhand_id_erhalten(self, quiz_id: int):
        return self.get_or_404(DBQuiz, quiz_id, "quizid")

    @router.post("/", response_model=Quiz_Response)
    def quiz_erstellen(self, quiz: Quiz_erstellen):
        db_quiz = DBQuiz(title=quiz.title, ordnerid=quiz.ordnerid)
        self.db.add(db_quiz)
        self.db.commit()
        self.db.refresh(db_quiz)
        print(self.db)
        return db_quiz


    @router.delete("/{quiz_id}")
    def quiz_entfernen(self, quiz_id: int):
        db_quiz = self.get_or_404(DBQuiz, quiz_id, "quizid")
        self.db.delete(db_quiz)
        self.db.commit()

    @router.put("/{quiz_id}", response_model=Quiz_Response)
    def quiz_veraendern(self, quiz_id: int, item: Quiz_erstellen):
        db_quiz= self.get_or_404(DBQuiz, quiz_id, "quizid")


        db_quiz.title = item.title
        db_quiz.ordnerid = item.ordnerid


        self.db.add(db_quiz)
        self.db.commit()
        self.db.refresh(db_quiz)

        return db_quiz


    @router.post("/ordner/{ordner_id}/generate")
    def quiz_aus_karteikarten_erstellen(self, ordner_id: int):
     karteikarten_holen = self.db.query(DBKarteikarte).filter(DBKarteikarte.ordnerid == ordner_id).all()
     return karteikarten_holen