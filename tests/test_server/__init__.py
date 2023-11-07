import asyncio
import os

os.environ["DEBUG"] = "1"


async def init_test():
    from server.models import init_db, add_user

    await init_db()
    user = await add_user(username="testuser", password="testpassword", is_admin=True)
    return user


TEST_USER = asyncio.run(init_test())
