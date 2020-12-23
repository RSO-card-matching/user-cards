from typing import Optional, List
from os import getenv

from sqlalchemy import create_engine, func
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
        user_id = 1,
        card_id = 0,
        state = "mint",
        wts = True
    ),
    models.SampleModel(
        id = 1,
        user_id = 1,
        card_id = 1,
        state = "scuffed",
        wts = False
    ),
    models.SampleModel(
        id = 2,
        user_id = 1,
        card_id = 1,
        state = "totally destroyed tbh",
        wts = True
    ),
    models.SampleModel(
        id = 3,
        user_id = 2,
        card_id = 0,
        state = "mint-ish, I guess",
        wts = False
    ),
    models.SampleModel(
        id = 4,
        user_id = 2,
        card_id = 0,
        state = "badly damaged",
        wts = True
    ),
    models.SampleModel(
        id = 5,
        user_id = 3,
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
        user_id =1,
        card_id = 2
    ),
    models.WishModel(
        id = 1,
        user_id = 2,
        card_id = 2
    ),
    models.WishModel(
        id = 2,
        user_id = 3,
        card_id = 1
    )]
    db.add_all(db_wishes)
    db.commit()
    db.close()


class DBException(Exception):
    pass



def get_sample_by_id(db: Session, sid: int) -> Optional[models.Sample]:
    card = db.query(models.SampleModel).filter(models.SampleModel.id == sid).first()
    if card:
        return models.Sample(**card.__dict__)
    return None


def get_all_samples(db: Session, uid: Optional[int], cid: Optional[int]) -> List[models.Sample]:
    q = db.query(models.SampleModel)
    if uid != None:
        q = q.filter(models.SampleModel.user_id == uid)
    if cid != None:
        q = q.filter(models.SampleModel.card_id == cid)
    return [models.Sample(**sample.__dict__) for sample in q.all()]


def insert_new_sample(db: Session, new_sample: models.SampleNew) -> int:
    new_id = db.query(func.max(models.SampleModel.id)).first()[0] + 1
    sample_model = models.SampleModel(
        id = new_id,
        user_id = new_sample.user_id,
        card_id = new_sample.card_id,
        state = new_sample.state,
        wts = new_sample.wts
    )
    db.add(sample_model)
    db.commit()
    return new_id


def update_sample(db: Session, sid: int, sample: models.SampleUpdate) -> None:
    sample_model = db.query(models.SampleModel).filter(models.SampleModel.id == sid).first()
    if sample_model == None:
        raise DBException
    if sample.user_id != None:
        sample_model.user_id = sample.user_id
    if sample.card_id != None:
        sample_model.card_id = sample.card_id
    if sample.state != None:
        sample_model.state = sample.state
    if sample.wts != None:
        sample_model.wts = sample.wts
    db.commit()


def delete_sample(db: Session, sid: int) -> None:
    sample_model = db.query(models.SampleModel).filter(models.SampleModel.id == sid)
    if sample_model.first() == None:
        raise DBException
    sample_model.delete()
    db.commit()




def get_wish_by_id(db: Session, wid: int) -> Optional[models.Wish]:
    card = db.query(models.WishModel).filter(models.WishModel.id == wid).first()
    if card:
        return models.Wish(**card.__dict__)
    return None


def get_all_wishes(db: Session, uid: Optional[int], cid: Optional[int]) -> List[models.Wish]:
    q = db.query(models.WishModel)
    if uid != None:
        q = q.filter(models.WishModel.user_id == uid)
    if cid != None:
        q = q.filter(models.WishModel.card_id == cid)
    return [models.Wish(**wish.__dict__) for wish in q.all()]


def insert_new_wish(db: Session, new_wish: models.WishNew) -> int:
    new_id = db.query(func.max(models.WishModel.id)).first()[0] + 1
    wish_model = models.WishModel(
        id = new_id,
        user_id = new_wish.user_id,
        card_id = new_wish.card_id
    )
    db.add(wish_model)
    db.commit()
    return new_id


def update_wish(db: Session, wid: int, wish: models.WishUpdate) -> None:
    wish_model = db.query(models.WishModel).filter(models.WishModel.id == wid).first()
    if wish_model == None:
        raise DBException
    if wish.user_id != None:
        wish_model.user_id = wish.user_id
    if wish.card_id != None:
        wish_model.card_id = wish.card_id
    db.commit()


def delete_wish(db: Session, wid: int) -> None:
    wish_model = db.query(models.WishModel).filter(models.WishModel.id == wid)
    if wish_model.first() == None:
        raise DBException
    wish_model.delete()
    db.commit()
