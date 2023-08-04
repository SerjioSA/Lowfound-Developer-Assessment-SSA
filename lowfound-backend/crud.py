from sqlalchemy.orm import Session

import models, schemas


def get_user(db: Session, username: str):
    # return db.query(models.User).filter(models.User.username == username).first()
    return db.query(models.User).filter(models.User.username == username).first()

def get_items_from_id(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Item).filter(models.Item.owner_id == owner_id).offset(skip).limit(limit).all()


def get_user_by_email(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, username = user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_last_item(db: Session):
    return db.query(models.Item).order_by(models.Item.id.desc()).first()

def delete_item_by_id(db: Session, item_id: int):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
