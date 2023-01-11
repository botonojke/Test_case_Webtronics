import sqlalchemy
import datetime
from db.base import metadata

posts = sqlalchemy.Table(
    'posts',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False),
    sqlalchemy.Column('title', sqlalchemy.String),
    sqlalchemy.Column('description', sqlalchemy.String),
    sqlalchemy.Column('is_active', sqlalchemy.Boolean, default=True),
    sqlalchemy.Column('create_date', sqlalchemy.DateTime, default=datetime.datetime.utcnow),
    sqlalchemy.Column('update_date', sqlalchemy.DateTime, default=datetime.datetime.utcnow),
)

post_rating = sqlalchemy.Table(
    'post_rating',
    metadata,
    sqlalchemy.Column('user_id', sqlalchemy.ForeignKey('users.id'), nullable=False),
    sqlalchemy.Column('post_id', sqlalchemy.ForeignKey('posts.id'), nullable=False),
    sqlalchemy.Column('likes', sqlalchemy.Boolean, default=None, nullable=True),
    sqlalchemy.Column('dislikes', sqlalchemy.Boolean, default=None, nullable=True)
)
