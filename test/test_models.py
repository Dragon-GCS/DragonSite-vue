import os
import unittest
from typing import List, Optional


os.environ["DEBUG"] = "True"

from random import choices
from unittest import IsolatedAsyncioTestCase

import sqlalchemy
from ormar.exceptions import NoMatch
from server.config import DATABASE_URL, FileCats
from server.models import User, UserData, add_user, drop_user
from server.models.base import metadata


print("Testing with database:", DATABASE_URL)


class TestModelBase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.engine = sqlalchemy.create_engine(DATABASE_URL)
        metadata.drop_all(self.engine)
        metadata.create_all(self.engine)

    # async def asyncTearDown(self):
    #     metadata.drop_all(self.engine)


class TestUsers(TestModelBase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.test_name, self.test_pwd = "test_name", "test_pws"

    async def test_add_user(self):
        await add_user(self.test_name, self.test_pwd, is_admin=True)
        user = await User.objects.get_or_none(username=self.test_name)
        assert user is not None
        self.assertTrue(user.validate_password(self.test_pwd))
        self.assertIsNotNone(await UserData.objects.get_or_none(path="/", owner=user))

        # test unique admin
        with self.assertRaises(ValueError):
            await add_user(self.test_pwd, self.test_name, is_admin=True)

    async def test_drop_user(self):
        user = await add_user(self.test_name, self.test_pwd, is_admin=True)
        await drop_user(self.test_name, self.test_pwd)
        with self.assertRaises(NoMatch):
            await User.objects.get(username=self.test_name)
            await UserData.objects.get(path="/", owner=user)


class TestUserData(TestModelBase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        await UserData.objects.get_or_create(path="/", is_dir=True)
        self.user = await User.objects.create(username="test", password="test")
        await UserData.objects.get_or_create(path="/", owner=self.user, is_dir=True)

        self.names = ["folder1", "folder2", "file1", "file2"]
        self.are_dir = [True, True, False, False]
        self.files_size = [0, 0, 1024, 1024]
        self.mime_types = ["application", "", "text/plain", "image/jpeg"]
        self.digests = [self.random_digest() for _ in range(len(self.names))]

    def random_digest(self):
        return "".join(choices("".join([chr(i) for i in range(97, 123)]), k=32))

    async def get_root(self):
        return await UserData.objects.get(path="/")

    async def _test_create(self, path: str, owner: Optional[User] = None):
        result = await UserData.create_resources(
            path, self.names, self.are_dir, self.files_size, self.mime_types, self.digests, owner
        )
        prefix = "" if path == "/" else path
        for i in range(len(result)):
            resource = result[i]
            self.assertEqual(resource.path, f"{prefix}/{self.names[i]}")
            self.assertEqual(resource.is_dir, self.are_dir[i])
            self.assertEqual(resource.file_size, 0 if resource.is_dir else self.files_size[i])
            self.assertEqual(resource.mime_type, "" if resource.is_dir else self.mime_types[i])
            if resource.digest:
                self.assertEqual(resource.digest.digest, self.digests[i])
            else:
                self.assertTrue(resource.is_dir)
        parent = await UserData.objects.get(path=path, owner=owner)
        self.assertEqual(await parent.children.count(), len(self.names))
        self.assertEqual(parent.file_size, sum(self.files_size))

    async def _test_get(
        self, path: str, category: FileCats = FileCats.ALL, owner: Optional[User] = None
    ):
        resources = await UserData.get_resources(path, category, owner)
        result_category = (
            [
                1
                for mime_type in self.mime_types
                if FileCats.sort_mime_type(mime_type) == category.value
            ]
            if category != FileCats.ALL
            else self.mime_types
        )
        self.assertEqual(len(resources), len(result_category))

    async def _test_rename(
        self, path: str, new_name: str, is_dir: bool, owner: Optional[User] = None
    ):
        result = await UserData.rename_resource(path, new_name, is_dir, owner)
        parent_path = path.rsplit("/", 1)[0]
        self.assertEqual(result.path, f"{parent_path}/{new_name}")
        self.assertEqual(result.name, new_name)

    async def _test_move(
        self,
        src_path: str,
        dst_path: str,
        names: List[str],
        are_dir: List[bool],
        owner: Optional[User] = None,
    ):
        result = await UserData.move_resources(src_path, dst_path, names, are_dir, owner)
        self.assertEqual(len(result), len(names))
        dst = "" if dst_path == "/" else dst_path
        for i in range(len(result)):
            self.assertEqual(result[i].parent_path, dst_path)
            self.assertEqual(result[i].path, f"{dst}/{names[i]}")

    async def _test_remove(
        self, paths: List[str], are_dir: List[bool], owner: Optional[User] = None
    ):
        await UserData.remove_resources(paths, are_dir, owner)
        for path, is_dir in zip(paths, are_dir):
            with self.assertRaises(NoMatch):
                await UserData.objects.get(path=path, is_dir=is_dir, owner=owner)

    async def test_crud(self):
        await self._test_create("/")
        await self._test_create("/" + self.names[0])
        await self._test_create("/", self.user)
        self.assertEqual(await UserData.objects.count(), len(self.names) * 3 + 2)

        await self._test_get("/" + self.names[0])
        await self._test_get("/" + self.names[0], FileCats.IMAGE)
        await self._test_get("/", owner=self.user)

        await self._test_move(
            "/" + self.names[0], "/" + self.names[1], self.names[2:], self.are_dir[2:]
        )
        await self._test_rename("/" + self.names[2], "new_file", self.are_dir[2])
        await self._test_rename("/" + self.names[0], "new_folder", self.are_dir[0])

        await self._test_remove(["/" + name for name in self.names], self.are_dir)


if __name__ == "__main__":
    unittest.main()
