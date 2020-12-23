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
async def return_all_samples(user_id: Optional[int] = None,
        card_id: Optional[int] = None,
        current_user: int = Depends(get_current_user_from_token),
        db: Session = Depends(get_db)):
    return database.get_all_samples(db, user_id, card_id)


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


@app.post("/v1/samples", response_model = models.NewSampleID)
async def create_new_sample(sample: models.SampleNew,
        current_user: int = Depends(get_current_user_from_token),
        db: Session = Depends(get_db)):
    new_id = database.insert_new_sample(db, sample)
    return models.NewSampleID(id = new_id)


@app.patch("/v1/samples/{sample_id}", response_model = None)
async def update_sample(to_update: models.SampleUpdate,
        sample_id: int = Path(...),
        current_user: int = Depends(get_current_user_from_token),
        db: Session = Depends(get_db)):
    try:
        database.update_sample(db, sample_id, to_update)
    except database.DBException:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Sample with given ID not found"
        )


@app.delete("/v1/samples/{sample_id}", response_model = None)
async def remove_sample(sample_id: int = Path(...),
        current_user: int = Depends(get_current_user_from_token),
        db: Session = Depends(get_db)):
    try:
        database.delete_sample(db, sample_id)
    except database.DBException:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Sample with given ID not found"
        )



@app.get("/v1/wishes", response_model = List[models.Wish])
async def return_all_wishes(user_id: Optional[int] = None,
        card_id: Optional[int] = None,
        current_user: int = Depends(get_current_user_from_token),
        db: Session = Depends(get_db)):
    return database.get_all_wishes(db, user_id, card_id)


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


@app.post("/v1/wishes", response_model = models.NewWishID)
async def create_new_wish(wish: models.WishNew,
        current_user: int = Depends(get_current_user_from_token),
        db: Session = Depends(get_db)):
    new_id = database.insert_new_wish(db, wish)
    return models.NewWishID(id = new_id)


@app.patch("/v1/wishes/{wish_id}", response_model = None)
async def update_wish(to_update: models.WishUpdate,
        wish_id: int = Path(...),
        current_user: int = Depends(get_current_user_from_token),
        db: Session = Depends(get_db)):
    try:
        database.update_wish(db, wish_id, to_update)
    except database.DBException:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Wish with given ID not found"
        )


@app.delete("/v1/wishes/{wish_id}", response_model = None)
async def remove_wish(wish_id: int = Path(...),
        current_user: int = Depends(get_current_user_from_token),
        db: Session = Depends(get_db)):
    try:
        database.delete_wish(db, wish_id)
    except database.DBException:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Wish with given ID not found"
        )



@app.get("/health/live", response_model = str)
async def liveness_check():
    return "OK"


@app.get("/health/ready", response_model = str)
async def readiness_check():
    return "OK"  # TODO: čekiranje baze or sth?
