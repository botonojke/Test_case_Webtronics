from typing import Optional

from fastapi import status, HTTPException, Depends, APIRouter

from endpoints.depends import get_current_user, get_posts_repository
from models.posts import Rate
from models.users import PublicUser
from repositories.posts import PostsRepository

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def rate_post(post_id: int,
                    rate: Rate,
                    post: PostsRepository = Depends(get_posts_repository),
                    current_user: PublicUser = Depends(get_current_user)) -> dict:
    """Add or remove like from foreign post"""
    # firstly check if post exist and user have sufficient rights
    posts = await post.get_by_id_post(id=post_id)
    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post was not found (id: {post_id})")
    if posts.user_id == int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="you can't rate your own post")
    # found rating
    rating = await post.get_post_rating(post_id=post_id, user_id=int(current_user.id))
    if rate.dir == 1:  # like post
        # return 409 if rating already exist
        if rating is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="rating already exist")
        await post.added_like(post_id=post_id, user_id=int(current_user.id))
    elif rate.dir == 2:  # dislike post
        # return 409 if rating already exist
        if rating is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="rating already exist")
        await post.added_dislike(post_id=post_id, user_id=int(current_user.id))
    elif rate.dir == 0:  # remove rating
        # return 404 if rating does not exist
        if rating is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="rating does not exist")
        await post.remove_rating(post_id=post_id, user_id=int(current_user.id))
    return {"detail": "rating is saved"}
