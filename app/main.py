# pylint: disable=no-name-in-module

from datetime import datetime, timedelta
from typing import Optional, List
from os import getenv

from fastapi import Depends, FastAPI, Form, HTTPException, Path, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import models, database


SECRET_KEY = getenv("OAUTH_SIGN_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

if (SECRET_KEY == None):
    print("Please define OAuth signing key!")
    exit(-1)

# fastAPI dependecy magic
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# init testing DB
# database.initBase(database.SessionLocal())

if (getenv("OAUTH_TOKEN_PROVIDER") == None):
    print("Please provide token provider URL!")
    exit(-1)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = getenv("OAUTH_TOKEN_PROVIDER") + "/tokens")

app = FastAPI()



async def get_current_user_from_token(token: str = Depends(oauth2_scheme)) -> int:
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        uid: Optional[int] = int(payload.get("sub"))
        if uid is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return uid



@app.get("/v1/samples", response_model = List[models.Sample])
async def return_all_samples(current_user: int = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)):
    return database.get_all_samples_by_user(db, current_user)


@app.get("/v1/samples/{sample_id}", response_model = models.Sample)
async def return_specific_sample(current_user: int = Depends(get_current_user_from_token),
    sample_id: int = Path(...),
    db: Session = Depends(get_db)):
    ret = database.get_sample_by_id(db, sample_id)
    if (ret == None):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Sample with given ID not found",
        )
    return ret


@app.get("/v1/wishes", response_model = List[models.Wish])
async def return_all_wishes(current_user: int = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)):
    return database.get_all_wishes_by_user(db, current_user)


@app.get("/v1/wishes/{wish_id}", response_model = models.Wish)
async def return_specific_wish(current_user: int = Depends(get_current_user_from_token),
    wish_id: int = Path(...),
    db: Session = Depends(get_db)):
    ret = database.get_wish_by_id(db, wish_id)
    if (ret == None):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Wish with given ID not found",
        )
    return ret


@app.get("/health/live", response_model = str)
async def liveness_check():
    return "OK"


@app.get("/health/ready", response_model = str)
async def readiness_check():
    return "OK"  # TODO: čekiranje baze or sth?
