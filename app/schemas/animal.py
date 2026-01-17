from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AnimalBase(BaseModel):
    species: str
    breed: Optional[str] = None
    sex: Optional[str] = None
    quantity: int

class AnimalCreate(AnimalBase):
    pass

class AnimalUpdate(BaseModel):
    species: Optional[str] = None
    breed: Optional[str] = None
    sex: Optional[str] = None
    quantity: Optional[int] = None

class AnimalOut(AnimalBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True





# from pydantic import BaseModel
# from datetime import datetime
# from typing import Optional

# class AnimalCreate(BaseModel):
#     species: str
#     breed: Optional[str] = None
#     sex: Optional[str] = None
#     quantity: int

# class AnimalResponse(BaseModel):
#     id: int
#     species: str
#     breed: Optional[str]
#     sex: Optional[str]
#     quantity: int
#     created_at: datetime

#     class Config:
#         from_attributes = True




# from pydantic import BaseModel
# from typing import Optional
# from datetime import datetime

# class AnimalCreate(BaseModel):
#     species: str
#     breed: Optional[str] = None
#     sex: Optional[str] = None  # "M" o "F"
#     quantity: int

# class AnimalResponse(AnimalCreate):
#     id: int
#     created_at: datetime

#     class Config:
#         orm_mode = True




