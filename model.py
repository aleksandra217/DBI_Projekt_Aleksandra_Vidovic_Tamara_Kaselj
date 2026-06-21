from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Date, UniqueConstraint
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime



class DBUser(Base):
    __tablename__ = 'users'

    userid = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email_adresse = Column(String(100), unique=True, nullable=False, index=True)
    passwort_hash = Column(String(255), nullable=False)
    rolle = Column(String(20), nullable=False, default="user")

    ordner = relationship("DBOrdner", back_populates="user")


class DBOrdner(Base):
    __tablename__ = 'ordner'

    ordnerid = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True)
    farbe = Column(String(30), nullable=True)
    userid = Column(Integer, ForeignKey('users.userid'), nullable=False)

    user = relationship("DBUser", back_populates="ordner")
    karteikarten = relationship("DBKarteikarte", back_populates="ordner")
    quizze = relationship("DBQuiz", back_populates="ordner")
    statistiken = relationship("DBStatistik", back_populates="ordner")



class DBKarteikarte(Base):
    __tablename__ = "karteikarten"

    karteikartenid = Column(Integer, primary_key=True, index=True)
    typ = Column(String(30), nullable=False)
    text_frage = Column(Text, index=True)
    text_loesung = Column(Text, index=True)
    ordnerid = Column(Integer, ForeignKey('ordner.ordnerid'), nullable=False)

    ordner = relationship("DBOrdner", back_populates="karteikarten")
    karteikarten_verbindung = relationship("DBQuizKarteikarte", back_populates="karteikarte")

class DBQuiz(Base):
    __tablename__ = "quiz"

    quizid = Column(Integer, primary_key=True)
    title = Column(String(100), index=True)
    ordnerid = Column(Integer, ForeignKey("ordner.ordnerid"), nullable=False)

    ordner = relationship("DBOrdner", back_populates="quizze")
    karteikarten_verbindungen = relationship("DBQuizKarteikarte", back_populates="quiz")



class DBQuizKarteikarte(Base):
    __tablename__ = "quiz_karteikarten"

    id = Column(Integer, primary_key=True, index=True)
    quizid = Column(Integer, ForeignKey("quiz.quizid"), nullable=False)
    karteikartenid = Column(Integer, ForeignKey("karteikarten.karteikartenid"), nullable=False)

    quiz = relationship("DBQuiz", back_populates="karteikarten_verbindungen")
    karteikarte = relationship("DBKarteikarte", back_populates="karteikarten_verbindung")

    __table_args__ = (
        UniqueConstraint("quizid", "karteikartenid", name="quiz_karte_unique"),
    )



class DBStatistik(Base):
    __tablename__ = "statistik"

    statistikid = Column(Integer, primary_key=True, index=True)
    ordnerid = Column(Integer, ForeignKey("ordner.ordnerid"), nullable=False)

    richtige_antworten = Column(Integer, nullable=False, default=0)
    falsche_antworten = Column(Integer, nullable=False, default=0)
    datum = Column(DateTime, nullable=False, default=datetime.now) # gibt die momentane zeit an.

    ordner = relationship("DBOrdner", back_populates="statistiken")



