from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class DBOrdner(Base):
    __tablename__ = 'ordner'

    ordnerid = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    userid = Column(Integer, ForeignKey('users.userid'))


