from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from repositories.users import UserRepository
from models.users import User, UserCreate, UserResponseId, UserUpdate, PublicUser
from endpoints.depends import get_user_repository, get_current_user

router = APIRouter()


@router.get("/", response_model=List[PublicUser])
async def read_users(
        users: UserRepository = Depends(get_user_repository),
        limit: int = 100,
        skip: int = 0) -> List[User]:
    return await users.get_all(limit=limit, skip=skip)


@router.post("/", response_model=UserResponseId)
async def create_user(
        user: UserCreate,
        users: UserRepository = Depends(get_user_repository)) -> UserResponseId:
    return await users.create(u=user)


@router.put("/", response_model=UserResponseId)
async def update_user(
        id: int,
        user: UserUpdate,
        users: UserRepository = Depends(get_user_repository),
        current_user: User = Depends(get_current_user)) -> UserResponseId:
    old_user = await users.get_by_id(id=id)
    if old_user is None or old_user.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found user')
    return await users.update(id=id, u=user)


@router.delete("/", response_model=UserResponseId)
async def delete_user(
        id: int,
        users: UserRepository = Depends(get_user_repository),
        current_user: User = Depends(get_current_user)) -> UserResponseId:
    old_user = await users.get_by_id(id=id)
    if old_user is None or old_user.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found user')
    await users.delete(id=id)
    return UserResponseId(id=id)
