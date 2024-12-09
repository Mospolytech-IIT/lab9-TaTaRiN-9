from models.models import User, Post, async_session

async def task2():
    async with async_session() as session:
        # Добавление пользователей
        user1 = User(username="airat", email="airat@test.com", password="pass")
        user2 = User(username="dima", email="dima@test.com", password="1234")
        session.add_all([user1, user2])
        session.commit()

        # Добавление постов
        post1 = Post(title="Пост Айрата 1", content="Здесь описание поста", user_id=user1.id)
        post2 = Post(title="Пост Айрата 2", content="Здесь какое-то описание", user_id=user1.id)
        post3 = Post(title="Пост Димы", content="Описание поста", user_id=user2.id)
        session.add_all([post1, post2, post3])
        session.commit()

        # Извлечение всех пользователей
        users = session.query(User).all()
        for user in users:
            print(user.username, user.email)

        # Извлечение всех постов с пользователями
        posts = session.query(Post).all()
        for post in posts:
            print(post.title, post.user.username)

        # Извлечение постов конкретного пользователя
        user_posts = session.query(Post).filter_by(user_id=user1.id).all()
        for post in user_posts:
            print(post.title)

        # Обновление email
        user_to_update = session.query(User).filter_by(username="airat").first()
        user_to_update.email = "new_airat@test.com"
        session.commit()

        # Обновление контента поста
        post_to_update = session.query(Post).filter_by(title="Пост Айрата 1").first()
        post_to_update.content = "Только что обновили описание"
        session.commit()

        print("Данные после обновления.")
        users = session.query(User).all()
        for user in users:
            print(user.username, user.email)

        posts = session.query(Post).all()
        for post in posts:
            print(post.title, post.user.username)

        post_to_delete = session.query(Post).filter_by(title="Пост Айрата 2").first()
        session.delete(post_to_delete)
        session.commit()

        # Удаление пользователя и его постов
        user_to_delete = session.query(User).filter_by(username="dima").first()
        session.query(Post).filter_by(user_id=user_to_delete.id).delete()
        session.delete(user_to_delete)
        session.commit()