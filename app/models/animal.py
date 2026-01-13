from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, text
from app.db.mysql import Base

class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    species = Column(String(50), nullable=False)
    breed = Column(String(50))
    sex = Column(Enum("M", "F"))
    quantity = Column(Integer, nullable=False)
    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )
