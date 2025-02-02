from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session

app = FastAPI()

hash_changer = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register/")
async def register(username: str, password: str, db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(Users.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Такое имя пользователя уже есть")
    
    hashed_password = hash_changer.hash(password)

    new_user = Users(username=username, hashed_password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Пользователь успешно зарегистрирован", "username": new_user.username}