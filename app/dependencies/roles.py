from fastapi import Depends, HTTPException, status
from app.dependencies.auth import get_current_user_from_cookie

def require_login(user=Depends(get_current_user_from_cookie)):
    return user

def require_admin(user=Depends(get_current_user_from_cookie)):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso solo para administradores"
        )
    return user

def require_tecnico(user=Depends(get_current_user_from_cookie)):
    if user["role"] not in ("admin", "tecnico"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso solo para técnicos"
        )
    return user

def require_operario(user=Depends(get_current_user_from_cookie)):
    if user["role"] not in ("admin", "operario"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso solo para operarios"
        )
    return user



