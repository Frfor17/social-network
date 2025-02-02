from database import Base
from sqlalchemy import Column, Integer, String

class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, index=True)
    username = Column(String)
    hashed_password = Column(String)

    