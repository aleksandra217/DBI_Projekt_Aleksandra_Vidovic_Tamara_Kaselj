from pydantic import BaseModel, field_validator, ConfigDict
from fastapi import APIRouter
from fastapi_restful.cbv import cbv


from users.model import DBUser
from users.base import BaseAPI




router = APIRouter(prefix="/user", tags=["User"])

class User_erstellen(BaseModel):
    name: str
    email_adresse: str


    @field_validator('name')
    @classmethod
    def ueberpruefen_ob_leerzeichen_vorhanden(cls, value: str):
        if not value.strip(): # entfernt die leerzeichen am anfang und am ende des namens.  Wenn kein Name eingegeben worden ist, dann wirft es einen Fehler.
            raise ValueError('Bitte gebe einen Namen ein.')
        return value

    @field_validator('email_adresse')
    @classmethod
    def ueberpruefen_ob_at_in_email(cls, value: str):
        if "@" in value:
            return value
        else:
            raise ValueError('Deine Email Adresse muss @ enthalten.')

class User_Response(User_erstellen):
    userid: int
    name: str
    email_adresse: str


    model_config = ConfigDict(from_attributes=True) # Greift auf die Daten von der DB zu.
@cbv(router)
class User_API(BaseAPI):
    @router.get("/", response_model=list[User_Response])
    def alle_user_erhalten(self):
        return self.db.query(DBUser).all()

    @router.get("/{user_id}", response_model=User_Response)
    def user_anhand_id_erhalten(self, user_id: int):
        return self.get_or_404(DBUser, user_id, "userid")

    @router.post("/", response_model=User_Response)
    def user_erstellen(self, user: User_erstellen):
        db_user = DBUser(name=user.name, email_adresse=user.email_adresse)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        print(self.db)
        return db_user


    @router.delete("/{user_id}")
    def user_entfernen(self, user_id: int):
        db_user = self.get_or_404(DBUser, user_id, "userid")
        self.db.delete(db_user)
        self.db.commit()

    @router.put("/{user_id}", response_model=User_Response)
    def user_veraendern(self, user_id: int, item: User_erstellen):
        db_user = self.get_or_404(DBUser, user_id, "userid")

        db_user.name = item.name
        db_user.email_adresse = item.email_adresse

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

