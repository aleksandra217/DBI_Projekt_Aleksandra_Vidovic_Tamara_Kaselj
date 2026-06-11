from pydantic import BaseModel, field_validator, ConfigDict
from fastapi import APIRouter, HTTPException, Query
from fastapi_restful.cbv import cbv
import hashlib


from model import DBUser
from base import BaseAPI




router = APIRouter(prefix="/user", tags=["User"])

def password_hash(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

class UserErstellen(BaseModel):
    name: str
    email_adresse: str
    passwort: str
    rolle: str = "user"


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

    @field_validator('passwort')
    @classmethod
    def passwort_pruefen(cls, value: str):
        if len(value) < 6:
            raise ValueError('Das Passwort muss mindenstens 6 Zeichen haben.')
        raise value


    @field_validator('rolle')
    @classmethod
    def rolle_pruefen(cls, value: str):
        if value not in ["user", "admin"]:
            raise ValueError("Rolle muss user ider admin sein")
        return value


class UserLogin(BaseModel):
    email_addresse: str
    password: str


class UserResponse(BaseModel):
    userid: int
    name: str
    email_adresse: str
    rolle: str


    model_config = ConfigDict(from_attributes=True) # Greift auf die Daten von der DB zu.

@cbv(router)
class UserAPI(BaseAPI):

    @router.get("/", response_model=list[UserResponse])
    def alle_user_erhalten(self, aktueller_user_id: int = Query(...)):
        self.check_admin(aktueller_user_id)
        return self.db.query(DBUser).all()

    @router.get("/{user_id}", response_model=UserResponse)
    def user_anhand_id_erhalten(self, user_id: int, aktueller_user_id: int = Query(...)):
        aktueller_user = self.get_or_404(DBUser, aktueller_user_id, "userid")

        if aktueller_user.rolle != "admin" and aktueller_user.userid != user_id:
            raise HTTPException(status_code=403, detail="Du darfst nur deinen eigenen User sehen.")

        return self.get_or_404(DBUser, user_id, "userid")

    @router.post("/", response_model=UserResponse, status_code=201)
    def user_erstellen(self, user: UserErstellen):
        user_vorhanden = self.db.query(DBUser).filter(
            DBUser.email_adresse == user.email_adresse
        ).first()

        if user_vorhanden:
            raise HTTPException(status_code=409, detail="Diese E-Mail gibt es schon.")

        db_user = DBUser(
            name=user.name,
            email_adresse=user.email_adresse,
            passwort_hash=password_hash(user.passwort),
            rolle=user.rolle
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    @router.post("/login")
    def login(self, login_daten: UserLogin):
        user = self.db.query(DBUser).filter(
            DBUser.email_adresse == login_daten.email_adresse
        ).first()

        if user is None:
            raise HTTPException(status_code=401, detail="E-Mail oder Passwort falsch.")

        if user.passwort_hash != password_hash(login_daten.passwort):
            raise HTTPException(status_code=401, detail="E-Mail oder Passwort falsch.")

        return {
            "message": "Login erfolgreich",
            "userid": user.userid,
            "rolle": user.rolle
        }

    @router.delete("/{user_id}")
    def user_entfernen(self, user_id: int, aktueller_user_id: int = Query(...)):
        self.check_admin(aktueller_user_id)

        db_user = self.get_or_404(DBUser, user_id, "userid")

        self.db.delete(db_user)
        self.db.commit()

        return {"message": "User wurde gelöscht."}

