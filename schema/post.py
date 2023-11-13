from typing import List, Optional

from sqlmodel import SQLModel


class PostBase(SQLModel):
    content: str
    media_url: str | None


class CreatePost(PostBase):
    pass


class CreatedPost(PostBase):
    id: int
    reaction: int


class CommentPostCreate(SQLModel):
    content: str


class ReadCommentPostCreate(SQLModel):
    id: int
    content: str
    post_id: int
    user_id: int
    reaction_count: int


class PostWithComment(CreatedPost):

    comments: List[CommentPostCreate]


class CommentReplyCreate(SQLModel):
    content: str


class ReadCommentReply(CommentReplyCreate):
    id: int
    comment_id: int
    user_id: int


class CommentReplyWithComment(ReadCommentReply):
    comment: Optional[CommentPostCreate]
