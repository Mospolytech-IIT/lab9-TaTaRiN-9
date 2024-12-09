from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from models.models import Base, User, Post, engine, get_session
from task2 import task2

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = FastAPI(on_startup=[init_db])

#
#  Задание 2
#
task2()


#
#  Задание 3
#
@app.post("/users/")
async def create_user(username: str, email: str, password: str, session: AsyncSession = Depends(get_session)):
    new_user = User(username=username, email=email, password=password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email}

@app.get("/users/")
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(text("SELECT * FROM users"))
    users = result.fetchall()
    return users

@app.get("/users/{user_id}")
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(text(f"SELECT * FROM users WHERE id = {user_id}"))
    user = result.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@app.post("/posts/")
async def create_post(title: str, content: str, user_id: int, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_post = Post(title=title, content=content, user_id=user_id)
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)
    return {"id": new_post.id, "title": new_post.title, "content": new_post.content}

@app.get("/posts/")
async def get_posts(session: AsyncSession = Depends(get_session)):
    result = await session.execute(text("SELECT * FROM posts"))
    posts = result.fetchall()
    return posts

@app.get("/posts/{post_id}")
async def get_post(post_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(text(f"SELECT * FROM posts WHERE id = {post_id}"))
    post = result.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post