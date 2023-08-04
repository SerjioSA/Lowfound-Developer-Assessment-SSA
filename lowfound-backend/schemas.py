from pydantic import BaseModel


class ItemBase(BaseModel):
    # title: str | None = None
    # description: str | None = None
    date: str
    question: str
    answer: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str | None = None
    username: str 


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int 
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
