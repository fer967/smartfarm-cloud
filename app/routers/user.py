from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.db.mysql import get_db
from app.models.user import User
# from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password
from app.dependencies.roles import require_admin
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def users_view(
    request: Request,
    user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    return templates.TemplateResponse(
        "users.html",
        {
            "request": request,
            "users": users,
            "user": user
        }
    )

@router.post("/create")
async def create_user(
    request: Request,
    user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    form = await request.form()
    new_user = User(
        username=form["username"],
        email=form["email"],
        role=form["role"],
        password_hash=hash_password(form["password"])
    )
    db.add(new_user)
    db.commit()
    return RedirectResponse("/users", status_code=302)

@router.post("/{user_id}/edit")
async def edit_user(
    user_id: int,
    request: Request,
    user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).get(user_id)
    if not db_user:
        raise HTTPException(status_code=404)
    form = await request.form()
    db_user.username = form["username"]
    db_user.email = form["email"]
    db_user.role = form["role"]
    db.commit()
    return RedirectResponse("/users", status_code=302)

@router.post("/{user_id}/delete")
def delete_user(
    user_id: int,
    user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).get(user_id)
    if not db_user:
        raise HTTPException(status_code=404)
    db.delete(db_user)
    db.commit()
    return RedirectResponse("/users", status_code=302)




