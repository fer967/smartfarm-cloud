from fastapi import Depends, HTTPException, status
from app.dependencies.auth import get_current_user_from_cookie

def require_admin_cookie(user=Depends(get_current_user_from_cookie)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403)
    return user

def require_tecnico_cookie(user=Depends(get_current_user_from_cookie)):
    if user["role"] not in ["tecnico", "admin"]:
        raise HTTPException(status_code=403)
    return user

def require_operario_cookie(user=Depends(get_current_user_from_cookie)):
    if user["role"] not in ["operario", "admin"]:
        raise HTTPException(status_code=403)
    return user
