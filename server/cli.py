import asyncio

from server.models import add_user, drop_user, init_db

asyncio.run(init_db())


def create_user(username: str, password: str, is_admin: bool):
    asyncio.run(add_user(username, password, is_admin))
    print(f"User {username} created")


def remove_user(username: str, password: str):
    asyncio.run(drop_user(username, password))
    print(f"User {username} removed")


if __name__ == "__main__":
    create_user("test", "test", True)