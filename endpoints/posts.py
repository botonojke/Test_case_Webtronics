from typing import List
from models.posts import Posts, Owner
from models.users import PublicUser
from repositories.posts import PostsRepository
from fastapi import APIRouter, Depends, HTTPException, status
from endpoints.depends import get_posts_repository, get_current_user

router = APIRouter()


@router.get("/", response_model=List[Posts])
async def show_all_posts(
        limit: int = 100,
        skip: int = 0,
        post: PostsRepository = Depends(get_posts_repository)) -> List[Posts]:
    return await post.all_posts(limit=limit, skip=skip)


@router.post("/", response_model=Posts)
async def create_post(
        owner: Owner,
        post: PostsRepository = Depends(get_posts_repository),
        current_user: PublicUser = Depends(get_current_user)) -> Posts:
    return await post.create_post(user_id=int(current_user.id), owner=owner)


@router.put("/", response_model=Posts)
async def update_post(
        id: int,
        owner: Owner,
        post: PostsRepository = Depends(get_posts_repository),
        current_user: PublicUser = Depends(get_current_user)) -> Posts:
    posts = await post.get_by_id_post(id=id)
    if posts is None or posts.user_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post is not found or you are not owner")
    return await post.update_post(id=id, user_id=int(current_user.id), owner=owner)


@router.delete("/")
async def delete_post(
        id: int,
        post: PostsRepository = Depends(get_posts_repository),
        current_user: PublicUser = Depends(get_current_user)):
    posts = await post.get_by_id_post(id=id)
    if posts is None or posts.user_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post is not found or you are not owner")
    await post.delete_post(id=id)
    return HTTPException(status_code=status.HTTP_200_OK, detail="Post deleted")

