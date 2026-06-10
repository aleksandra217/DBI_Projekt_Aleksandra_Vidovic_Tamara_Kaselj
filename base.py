from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from model import DBUser, DBOrdner

class BaseAPI:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_or_404(self, model, item_id: int, id_field: str):
        item = self.db.query(model).filter(getattr(model, id_field) == item_id).first()

        if item is None:
            raise HTTPException(status_code=404,
                                detail=f"Eintrag mit der ID {item_id}wurde nicht gefunden.")

        return item

    def check_admin(self, user_id: int):
        user = self.get_or_404(DBUser,user_id, "userid")

        if user.rolle != "admin":
            raise HTTPException(
                status_code=403,
            detail="Nur Admins dürfen das machen."
            )
        return user


    def check_ordner_besitzer_oder_admin(self, ordner_id: int, user_id: int):
        user = self.get_or_404(DBUser, user_id, "ordnerid")
        ordner = self.get_or_404(DBOrdner,ordner_id, "ordnerid")

        if user.rolle == "admin":
            return ordner


        if ordner.userid != user.userid:
            raise HTTPException(
                status_code=403,
                detail="Du darfst diesen Ordner nicht berarbeiten"
            )

        return ordner