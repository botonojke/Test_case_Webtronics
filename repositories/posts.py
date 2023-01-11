from repositories.base import BaseRepository
from models.posts import Posts, Owner, Rate, Rating
import datetime
from typing import List, Optional
from db.posts import posts, post_rating


class PostsRepository(BaseRepository):

    async def create_post(self, user_id: int, owner: Owner) -> Posts:
        post = Posts(
            id=0,
            user_id=user_id,
            create_date=datetime.datetime.utcnow(),
            update_date=datetime.datetime.utcnow(),
            title=owner.title,
            description=owner.description,
            is_active=owner.is_active,
        )
        values = {**post.dict()}
        values.pop("id", None)
        query = posts.insert().values(**values)
        posts.id = await self.database.execute(query=query)
        return post

    async def update_post(self, id: int, user_id: int, owner: Owner) -> Posts:
        post = Posts(
            id=id,
            user_id=user_id,
            update_date=datetime.datetime.utcnow(),
            create_date=datetime.datetime.utcnow(),
            title=owner.title,
            description=owner.description,
            is_active=owner.is_active,
        )
        values = {**post.dict()}
        values.pop("create_date", None)
        values.pop("id", None)
        query = posts.update().where(posts.c.id == id).values(**values)
        await self.database.execute(query=query)
        return post

    async def all_posts(self, limit: int = 100, skip: int = 0) -> List[Posts]:
        query = posts.select().limit(limit).offset(skip).where(posts.c.is_active)
        data = await self.database.fetch_all(query=query)
        return [Posts(**item) for item in data]

    async def delete_post(self, id: int):
        query = posts.delete().where(posts.c.id == id)
        return await self.database.execute(query=query)

    async def get_by_id_post(self, id: int) -> Optional[Posts]:
        query = posts.select().where(posts.c.id == id)
        post = await self.database.fetch_one(query=query)
        if post is None:
            return None
        return Posts.parse_obj(post)

    # async def like_post(self, post_id: int, rate: Rate):
    #     rating = Rate(
    #         post_id=post_id,
    #         like=rate.like,
    #         dislike=rate.dislike
    #     )
    #     values = {**rating.dict()}
    #     query = post_rating.insert().values(**values)
    #     await self.database.execute(query=query)
    #     return rating

    async def get_post_rating(self, post_id: int, user_id: int) -> Rating:
        query = posts.select().where(post_rating.c.post_id == post_id, post_rating.c.user_id == user_id)
        post = await self.database.fetch_one(query=query)
        if post is None:
            return None
        return Rating.parse_obj(post)

    async def added_like(self, post_id: int, user_id: int) -> Rating:
        rating = Rating(
                post_id=post_id,
                user_id=user_id,
                like=True,
                dislike=False
            )
        values = {**rating.dict()}
        query = post_rating.insert().values(**values)
        await self.database.execute(query=query)
        return rating

    async def added_dislike(self, post_id: int, user_id: int) -> Rating:
        rating = Rating(
                post_id=post_id,
                user_id=user_id,
                like=False,
                dislike=True
            )
        values = {**rating.dict()}
        query = post_rating.insert().values(**values)
        await self.database.execute(query=query)
        return rating

    async def remove_rating(self, post_id: int, user_id: int):
        query = post_rating.delete().where(post_rating.c.post_id == post_id, post_rating.c.user_id == user_id)
        return await self.database.execute(query=query)

