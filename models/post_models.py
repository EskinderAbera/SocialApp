import datetime
from typing import Optional, List

from sqlalchemy import Index
from sqlmodel import SQLModel, Field, Relationship

from models.user_models import User


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(index=True)
    media_url: Optional[str] = None
    user_id: Optional[int] = Field(default=None, foreign_key='user.id')
    user: Optional[User] = Relationship()
    reaction: int = 0

    comments: List["Comment"] = Relationship(back_populates="post")

    reactions: List["PostReaction"] = Relationship(back_populates="post")


class PostReaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key='user.id')
    post_id: Optional[int] = Field(default=None, foreign_key='post.id')

    post: Optional[Post] = Relationship(back_populates="reactions")


class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(index=True)
    post_id: Optional[int] = Field(default=None, foreign_key='post.id')
    user_id: Optional[int] = Field(default=None, foreign_key='user.id')
    user: Optional[User] = Relationship()
    reaction_count: int = 0

    post: Optional[Post] = Relationship(back_populates="comments")

    replies: List["CommentReply"] = Relationship(back_populates="comment")


class CommentReaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key='user.id')
    comment_id: Optional[int] = Field(default=None, foreign_key='comment.id')


class CommentReply(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    comment_id: Optional[int] = Field(default=None, foreign_key='comment.id')
    user_id: Optional[int] = Field(default=None, foreign_key='user.id')
    user: Optional[User] = Relationship()

    comment: Optional[Comment] = Relationship(back_populates="replies")

    # You might want to include the post_id if replies are to be associated directly with a post.
    # post_id: Optional[int] = Field(default=None, foreign_key='post.id')

