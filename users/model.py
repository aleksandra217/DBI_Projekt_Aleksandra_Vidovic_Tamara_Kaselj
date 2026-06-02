from sqlalchemy import Column, Integer, String
from database import Base

class DBUser(Base):
    __tablename__ = 'users'

    userid = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    email_adresse = Column(String, index=True)