import datetime
from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, validator, constr


class Posts(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    is_active: bool = True
    create_date: datetime.datetime
    update_date: datetime.datetime


class Owner(BaseModel):
    title: str
    description: str
    is_active: bool = True


class Rate(BaseModel):
    dir: Literal[0, 1, 2]  # direction: 0 - remove, 1 - like, 2 - dislike


class Rating(BaseModel):
    post_id: int
    user_id: int
    like: bool
    dislike: bool
