from sqlalchemy import Column, Integer, String, ForeignKey, Date
from database import Base


class DBUser(Base):
    __tablename__ = 'users'

    userid = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    email_adresse = Column(String, index=True)





class DBOrdner(Base):
    __tablename__ = 'ordner'

    ordnerid = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    userid = Column(Integer, ForeignKey('users.userid'))


from sqlalchemy import Column, Integer, Text, ForeignKey
from database import Base


class DBKarteikarten(Base):
    __tablename__ = "karteikarten"

    karteikartenid = Column(Integer, primary_key=True)
    text_frage = Column(Text, index=True)
    text_loesung = Column(Text, index=True)
    ordnerid = Column(Integer, ForeignKey('ordner.ordnerid'))



class DBQuiz(Base):
    __tablename__ = "quiz"

    quizid = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    ordnerid = Column(Integer, ForeignKey("ordner.ordnerid"))


class DBQuizFrage_und_Antwort(Base):
    __tablename__ = "quizfrage_und_antwort"

    frageid = Column(Integer, primary_key=True)
    frage = Column(String)
    antwort = Column(String)

    quizid = Column(Integer, ForeignKey("quiz.quizid"))


class DBStatistik(Base):

    __tablename__ = "statistik"
    statistikid = Column(Integer, primary_key=True)
    ordnerid = Column(Integer, ForeignKey("ordner.ordnerid"))
    richtige_antworten = Column(Integer)
    falsche_antworten = Column(Integer)
    aktualisierungsstatistik = Column(Date)



