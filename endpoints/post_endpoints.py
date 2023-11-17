from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import func
from sqlmodel import select, Session, col
from starlette.responses import JSONResponse
from starlette.status import *
import socket
from db.db import get_session, db
from endpoints.user_endpoints import auth_handler
from models.post_models import Post, PostReaction, Comment, CommentReaction, CommentReply
from schema.post import CreatePost, CreatedPost, CommentPostCreate, ReadCommentPostCreate, \
    PostWithComment, CommentReplyCreate, ReadCommentReply, CommentReplyWithComment

post_router = APIRouter()


@post_router.get('/')
def greet():
    return f"Container ID: {socket.gethostname()}"


@post_router.post('/post', tags=["Posts"], response_model=CreatedPost)
def posts(*, session: Session = Depends(get_session), post: CreatePost, user=Depends(auth_handler.get_current_user)):
    if not user:
        print("no user", user)
        return JSONResponse({'msg': 'unauthorized'}, status_code=HTTP_401_UNAUTHORIZED)
    post = Post(user_id=user.id, content=post.content, media_url=post.media_url)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@post_router.get('/post', tags=["Posts"], response_model=List[PostWithComment])
def list_of_posts(*, session: Session = Depends(get_session), user=Depends(auth_handler.get_current_user),
                  page: int = Query(1, ge=1),
                  page_size: int = Query(10, le=50), ):
    # statement = select(Post).where(col(Post.user_id) != user.id)
    # list_posts = session.exec(statement).all()
    skip = (page - 1) * page_size
    stmt = select(Post).where(col(Post.user_id) == user.id).offset(skip).limit(page_size)
    # statement = select(Post).where(col(Post.user_id) == user.id)
    list_posts = session.exec(stmt).all()
    return list_posts


@post_router.post("/post/react/{id}", tags=["Posts"], response_model=CreatedPost)
def react_post(*, session: Session = Depends(get_session), post_id: int, user=Depends(auth_handler.get_current_user)):
    post_found = session.get(Post, post_id)
    if not post_found:
        return JSONResponse({"msg": "Post does not exist"}, status_code=HTTP_404_NOT_FOUND)
    statement = select(PostReaction).where(col(PostReaction.post_id) == post_found.id,
                                           col(PostReaction.user_id) == user.id)
    reacted_posts = session.exec(statement)
    reacted_post = reacted_posts.first()
    if not reacted_post:
        create_post = PostReaction(user_id=user.id, post_id=post_found.id)
        post_found.reaction = post_found.reaction + 1
        session.add(post_found)
        session.add(create_post)
    else:
        session.delete(reacted_post)
        post_found.reaction = post_found.reaction - 1
        session.add(post_found)
    session.commit()
    return JSONResponse({"msg": "reacted successfully"}, status_code=HTTP_200_OK)


@post_router.get("/post/mine", tags=["Posts"], response_model=List[PostWithComment])
def list_of_my_posts(*, session: Session = Depends(get_session),
                     user=Depends(auth_handler.get_current_user), page: int = Query(1, ge=1),
                     page_size: int = Query(10, le=50), ):
    skip = (page - 1) * page_size
    stmt = select(Post).where(col(Post.user_id) == user.id).offset(skip).limit(page_size)
    # statement = select(Post).where(col(Post.user_id) == user.id)
    list_posts = session.exec(stmt).all()
    return list_posts


@post_router.post("/post/comment/{id}", tags=["Posts"], response_model=ReadCommentPostCreate)
def comment_post(*, session: Session = Depends(get_session), user=Depends(auth_handler.get_current_user),
                 post_id: int, comment: CommentPostCreate):
    post = session.get(Post, post_id)
    if not post:
        return JSONResponse({"msg": "Post does not exist"}, status_code=HTTP_404_NOT_FOUND)
    if post.user_id == user.id:
        return JSONResponse({"msg": "you can't comment your own posts"}, status_code=HTTP_400_BAD_REQUEST)
    commented_post = Comment(user_id=user.id, post_id=post_id, content=comment.content)
    session.add(commented_post)
    session.commit()
    session.refresh(commented_post)
    return commented_post


@post_router.post("/post/comment/react/{id}", tags=["Posts"])
def comment_reaction(*, session: Session = Depends(get_session), user=Depends(auth_handler.get_current_user),
                     comment_id: int):
    comment = session.get(Comment, comment_id)
    if not comment:
        return JSONResponse({"msg": "Comment does not exist"}, status_code=HTTP_404_NOT_FOUND)
    statement = select(CommentReaction).where(col(CommentReaction.comment_id) == comment_id,
                                              col(CommentReaction.user_id) == user.id)
    reacted_comments = session.exec(statement)
    reacted_comment = reacted_comments.first()

    if not reacted_comment:
        create_react = CommentReaction(user_id=user.id, comment_id=comment_id)
        comment.reaction_count = comment.reaction_count + 1
        session.add(comment)
        session.add(create_react)
    else:
        session.delete(reacted_comment)
        comment.reaction_count = comment.reaction_count - 1
        session.add(comment)
    session.commit()
    return JSONResponse({"msg": "reacted successfully"}, status_code=HTTP_200_OK)


@post_router.post("/post/comment/reply/{id}", tags=["Posts"], response_model=ReadCommentReply)
def comment_reply(*, session: Session = Depends(get_session), user=Depends(auth_handler.get_current_user),
                  comment_id: int, comment_input: CommentReplyCreate):
    comment = session.get(Comment, comment_id)
    if not comment:
        return JSONResponse({"msg": "Comment does not exist"}, status_code=HTTP_404_NOT_FOUND)

    create_comment_reply = CommentReply(user_id=user.id, comment_id=comment_id, content=comment_input.content)
    session.add(create_comment_reply)
    session.commit()
    session.refresh(create_comment_reply)

    return create_comment_reply


@post_router.get("/post/comment/reply/{id}", tags=["Posts"], response_model=List[CommentReplyWithComment])
def get_comment_reply(*, session: Session = Depends(get_session), user=Depends(auth_handler.get_current_user),
                      comment_id: int):
    statement = select(CommentReply).where(col(CommentReply.comment_id) == comment_id)
    result = session.exec(statement).all()
    return result


@post_router.get("/search", tags=["Search"])
def search_posts_and_comments(*, user=Depends(auth_handler.get_current_user),
                              search_query: str):
    query = f"""
            SELECT * FROM post
            WHERE search_vector @@ to_tsquery('english', :search_query)
        """
    fetched_posts = db.execute(query, {"search_query": search_query}).fetchall()
    if not fetched_posts:
        raise HTTPException(status_code=404, detail="No posts found")
    return fetched_posts
