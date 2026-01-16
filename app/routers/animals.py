from fastapi import (
    APIRouter, Depends, HTTPException, Request
)
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.animal import Animal
from app.dependencies.roles import require_operario
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/animals",
    tags=["Animals"]
)

templates = Jinja2Templates(directory="app/templates")

# 📄 Vista principal
@router.get("/view", response_class=HTMLResponse)
def animals_view(
    request: Request,
    user=Depends(require_operario),
    db: Session = Depends(get_db)
):
    animals = db.query(Animal).all()
    return templates.TemplateResponse(
        "animals.html",
        {
            "request": request,
            "animals": animals,
            "user": user
        }
    )


# ➕ Crear
@router.post("/create")
async def create_animal(
    request: Request,
    user=Depends(require_operario),
    db: Session = Depends(get_db)
):
    form = await request.form()
    animal = Animal(
        species=form["species"],
        breed=form.get("breed"),
        sex=form.get("sex"),
        quantity=int(form["quantity"])
    )
    db.add(animal)
    db.commit()
    return RedirectResponse("/animals/view", status_code=302)


# ✏️ Editar
@router.post("/{animal_id}/edit")
async def edit_animal(
    animal_id: int,
    request: Request,
    user=Depends(require_operario),
    db: Session = Depends(get_db)
):
    animal = db.query(Animal).get(animal_id)
    if not animal:
        raise HTTPException(status_code=404)
    form = await request.form()
    animal.species = form["species"]
    animal.breed = form.get("breed")
    animal.sex = form.get("sex")
    animal.quantity = int(form["quantity"])
    db.commit()
    return RedirectResponse("/animals/view", status_code=302)


# 🗑️ Eliminar
@router.post("/{animal_id}/delete")
def delete_animal(
    animal_id: int,
    user=Depends(require_operario),
    db: Session = Depends(get_db)
):
    animal = db.query(Animal).get(animal_id)
    if not animal:
        raise HTTPException(status_code=404)
    db.delete(animal)
    db.commit()
    return RedirectResponse("/animals/view", status_code=302)



# from fastapi import APIRouter, Depends, HTTPException, Query, Request
# from fastapi.responses import HTMLResponse, RedirectResponse
# from sqlalchemy.orm import Session
# from typing import List, Optional
# from app.db.mysql import get_db
# from app.models.animal import Animal
# from app.schemas.animal import AnimalCreate, AnimalUpdate, AnimalOut
# from app.dependencies.roles import require_operario
# from fastapi.templating import Jinja2Templates

# router = APIRouter(
#     prefix="/animals",
#     tags=["Animals"]
# )

# templates = Jinja2Templates(directory="app/templates")

# @router.get("/view", response_class=HTMLResponse)
# def animals_view(
#     request: Request,
#     user=Depends(require_operario),
#     db: Session = Depends(get_db)
# ):
#     animals = db.query(Animal).all()

#     return templates.TemplateResponse(
#         "animals.html",
#         {
#             "request": request,
#             "animals": animals,
#             "user": user
#         }
#     )

# @router.get("/", response_model=List[AnimalOut])
# def get_animals(
#     species: Optional[str] = Query(None, description="Filtrar por especie"),
#     sex: Optional[str] = Query(None, description="M o F"),
#     min_quantity: Optional[int] = Query(None, description="Cantidad mínima"),
#     user=Depends(require_operario),   # 🔐 PROTEGIDO
#     db: Session = Depends(get_db)
# ):
#     query = db.query(Animal)
#     if species:
#         query = query.filter(Animal.species == species)
#     if sex:
#         query = query.filter(Animal.sex == sex)
#     if min_quantity is not None:
#         query = query.filter(Animal.quantity >= min_quantity)
#     return query.all()

# @router.post("/", response_model=AnimalOut, status_code=201)
# def create_animal(
#     animal: AnimalCreate,
#     db: Session = Depends(get_db), user=Depends(require_operario)
# ):
#     db_animal = Animal(**animal.model_dump())
#     db.add(db_animal)
#     db.commit()
#     db.refresh(db_animal)
#     return db_animal

# @router.put("/{animal_id}", response_model=AnimalOut)
# def update_animal(
#     animal_id: int,
#     animal: AnimalUpdate,
#     db: Session = Depends(get_db), user=Depends(require_operario)
# ):
#     db_animal = db.query(Animal).filter(Animal.id == animal_id).first()
#     if not db_animal:
#         raise HTTPException(status_code=404, detail="Animal not found")
#     for field, value in animal.model_dump(exclude_unset=True).items():
#         setattr(db_animal, field, value)
#     db.commit()
#     db.refresh(db_animal)
#     return db_animal

# @router.delete("/{animal_id}", status_code=204)
# def delete_animal(
#     animal_id: int,
#     db: Session = Depends(get_db), user=Depends(require_operario)
# ):
#     db_animal = db.query(Animal).filter(Animal.id == animal_id).first()
#     if not db_animal:
#         raise HTTPException(status_code=404, detail="Animal not found")
#     db.delete(db_animal)
#     db.commit()













