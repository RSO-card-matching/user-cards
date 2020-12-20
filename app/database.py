from typing import Optional, List
from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from . import models


db_ip = getenv("DATABASE_IP")
if db_ip:
    SQLALCHEMY_DATABASE_URL = db_ip
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# temporary, for testing
def initBase(db: Session):
    engine = db.get_bind()
    try:
        models.SampleModel.__table__.drop(engine)
    except:
        pass
    models.SampleModel.__table__.create(engine)
    db_cards = [models.SampleModel(
        id = 0,
        user_id = 0,
        card_id = 0,
        state = "mint",
        wts = True
    ),
    models.SampleModel(
        id = 1,
        user_id = 0,
        card_id = 1,
        state = "scuffed",
        wts = False
    ),
    models.SampleModel(
        id = 2,
        user_id = 0,
        card_id = 1,
        state = "totally destroyed tbh",
        wts = True
    ),
    models.SampleModel(
        id = 3,
        user_id = 1,
        card_id = 0,
        state = "mint-ish, I guess",
        wts = False
    ),
    models.SampleModel(
        id = 4,
        user_id = 1,
        card_id = 0,
        state = "badly damaged",
        wts = True
    ),
    models.SampleModel(
        id = 5,
        user_id = 2,
        card_id = 2,
        state = "has a hole in it, but basically mint otherwise",
        wts = True
    )]
    db.add_all(db_cards)
    db.commit()

    try:
        models.WishModel.__table__.drop(engine)
    except:
        pass
    models.WishModel.__table__.create(engine)
    db_wishes = [models.WishModel(
        id = 0,
        user_id = 0,
        card_id = 2
    ),
    models.WishModel(
        id = 1,
        user_id = 1,
        card_id = 2
    ),
    models.WishModel(
        id = 2,
        user_id = 2,
        card_id = 1
    )]
    db.add_all(db_wishes)
    db.commit()
    db.close()



def get_sample_by_id(db: Session, sid: int) -> Optional[models.Sample]:
    card = db.query(models.SampleModel).filter(models.SampleModel.id == sid).first()
    if card:
        return models.Sample(**card.__dict__)
    return None


def get_all_samples_by_user(db: Session, uid: int) -> List[models.Sample]:
    return [
        models.Sample(**sample.__dict__)
        for sample
        in db.query(models.SampleModel).filter(models.SampleModel.user_id == uid).all()
    ]

def get_wish_by_id(db: Session, wid: int) -> Optional[models.Wish]:
    card = db.query(models.WishModel).filter(models.WishModel.id == wid).first()
    if card:
        return models.Wish(**card.__dict__)
    return None


def get_all_wishes_by_user(db: Session, uid: int) -> List[models.Wish]:
    return [
        models.Wish(**wish.__dict__)
        for wish
        in db.query(models.WishModel).filter(models.WishModel.user_id == uid).all()
    ]
