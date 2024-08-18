from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import schemas, models, crud, oauth2
from app.database import get_db
from app.utils import hash_password, verify_password

router = APIRouter()

# Registration Endpoint
@router.post("/register", response_model=schemas.UserWithToken)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = hash_password(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password, role=user.role, is_active=True)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate the access token
    token = oauth2.create_access_token(data={"sub": new_user.username})

    # Return the user details and the access token
    return {
        "username": new_user.username,
        "id": new_user.id,
        "is_active": new_user.is_active,
        "role": new_user.role,  # Include role in the response
        "access_token": token
    }

@router.post("/login", response_model=schemas.UserWithToken)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = oauth2.create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,  # Include username in the response
        "id": user.id,              # Include id in the response
        "is_active": user.is_active,
        "role": user.role           # Include role in the response
    }
# Get Current User Endpoint
@router.get("/users/me", response_model=schemas.User)
def get_me(current_user: schemas.User = Depends(oauth2.get_current_user)):
    return current_user




