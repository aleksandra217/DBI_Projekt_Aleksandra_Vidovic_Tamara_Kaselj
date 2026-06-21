from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db

class BaseAPI:
    # Wieso bekomme ich die ganze zeit einen fehler bei get_db? /Aleksandra
    # damit man später auf das db zugreifen kann und nicht im router.py erstellen muss, kann man es auch hier erstellen und dann bei router.py darauf zugreifen.
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_or_404(self, model, item_id: int, id_field: str):
        # Wieso funktioniert diese Zeile code nicht? / Aleksandra
        # getattr ... sucht in der DB nach der user_id spalte und wenn es diese gefunden hat, dann schaut es die restlichen eigenschaften des users wie name und email-adresse an.
        item = self.db.query(model).filter(getattr(model, id_field) == item_id).first()

        if not item:
            raise HTTPException(status_code=404, detail=f"Der Eintrag in {model.__tablename__} mit der ID {item_id} konnte nicht gefunden werden.")
        return item