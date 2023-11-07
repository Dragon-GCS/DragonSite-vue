import asyncio
import unittest
from io import BytesIO
from pathlib import Path

from fastapi.testclient import TestClient
from PIL import Image

from server import app
from server.config import THUMBNAIL_SIZE, FileTypeEnum
from server.models import FileInfo, UserData, database
from server.schemas.disk import Resource

from . import TEST_USER


class TestDisk(unittest.IsolatedAsyncioTestCase):
    async def clear_data(self):
        """Clear all data in database except root directory"""
        await UserData.objects.exclude(parent=None).delete()
        await FileInfo.objects.delete(each=True)

    async def asyncSetUp(self):
        # disable debug mode
        asyncio.get_running_loop().set_debug(False)

        self.client = TestClient(app, base_url="http://testserver/api/disk")
        self.client.post("http://testserver/api/auth/login", data=TEST_USER.dict())

        self.public_root = await UserData.objects.get(name="/", owner=None, is_dir=True)
        self.private_root = await UserData.objects.get(name="/", owner=TEST_USER, is_dir=True)
        await self.clear_data()

    @database.transaction(force_rollback=True)
    async def test_get_resources(self):
        # fake data
        fake_folder = await UserData(
            name="test", owner=TEST_USER, is_dir=True, parent=self.private_root
        ).save()
        meta = await FileInfo(
            digest="098f6bcd4621d373cade4e832627b4f6", category="text", mime_type="text/plain"
        ).save()
        fake_file = await UserData(
            name="test.txt", owner=TEST_USER, is_dir=False, meta=meta, parent=self.private_root
        ).save()
        # list resources
        response = self.client.get(
            "resources", params={"path": self.private_root.id.hex, "login_require": True}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

        for res in response.json():
            return_resource = Resource(**res)
            compare_resource = fake_folder if return_resource.is_dir else fake_file
            self.assertEqual(return_resource, Resource(**compare_resource.dict()))
        # list resources in public root
        self.assertEqual(
            self.client.get("resources", params={"path": self.public_root.id.hex}).json(), []
        )
        # list resources with category
        response = self.client.get(
            "resources",
            params={
                "path": self.private_root.id.hex,
                "login_require": True,
                "category": FileTypeEnum.TEXT.value,
            },
        ).json()
        self.assertEqual(len(response), 1)
        self.assertEqual(Resource(**response[0]), Resource(**fake_file.dict()))

    @database.transaction(force_rollback=True)
    async def test_create_folder(self):
        response = self.client.post(
            "resources", params={"path": self.public_root.id.hex, "name": "test_dir"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            await UserData.objects.filter(
                name="test_dir", owner=None, parent=self.public_root
            ).exists()
        )

    @database.transaction(force_rollback=True)
    async def test_create_file(self):
        response = self.client.post(
            "resources",
            params={"path": self.private_root.id.hex, "login_require": True},
            files={"files": ("test.txt", b"test")},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            await UserData.objects.filter(
                name="test.txt", owner=TEST_USER, parent=self.private_root
            ).exists()
        )
        self.assertTrue(
            await FileInfo.objects.filter(digest="098f6bcd4621d373cade4e832627b4f6").exists()
        )
        digest = await FileInfo.objects.get(digest="098f6bcd4621d373cade4e832627b4f6")
        await digest.delete()

    @database.transaction(force_rollback=True)
    async def test_delete_resources(self):
        # create fake data
        await UserData(name="test", owner=TEST_USER, is_dir=True, parent=self.private_root).save()
        meta = await FileInfo(
            digest="098f6bcd4621d373cade4e832627b4f6", category="text", mime_type="text/plain"
        ).save()
        await UserData(
            name="test.txt", owner=TEST_USER, is_dir=False, meta=meta, parent=self.private_root
        ).save()

        # delete the fake data
        response = self.client.delete(
            "resources",
            params={
                "path": self.private_root.id.hex,
                "names": ["test", "test.txt"],
                "login_require": True,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)
        # check that the fake data was deleted
        self.assertFalse(
            await UserData.objects.filter(
                name="test", owner=TEST_USER, parent=self.private_root
            ).exists()
        )
        self.assertFalse(
            await UserData.objects.filter(
                name="test.txt", owner=TEST_USER, parent=self.private_root
            ).exists()
        )

    @database.transaction(force_rollback=True)
    async def test_modify_resource(self):
        # create fake data
        self.client.post("resources", params={"path": self.private_root.id.hex, "name": "test1"})
        folder = await UserData(
            name="test1", owner=TEST_USER, is_dir=True, parent=self.private_root
        ).save()
        meta = await FileInfo(
            digest="098f6bcd4621d373cade4e832627b4f6", category="text", mime_type="text/plain"
        ).save()
        file = await UserData(
            name="file1.txt", owner=TEST_USER, is_dir=False, meta=meta, parent=folder
        ).save()
        # rename resources
        response = self.client.patch(
            "resources",
            json={
                "src": [folder.id.hex, file.id.hex],
                "names": ["new_test1", "new_file1.txt"],
            },
            params={"path": self.private_root.id.hex, "login_require": True},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

        # check that resources were renamed
        self.assertFalse(
            await UserData.objects.filter(
                name="test1", owner=TEST_USER, parent=self.private_root
            ).exists()
        )
        self.assertTrue(
            await UserData.objects.filter(
                name="new_test1", owner=TEST_USER, parent=self.private_root
            ).exists()
        )

        self.assertFalse(
            await UserData.objects.filter(name="file1.txt", owner=TEST_USER, parent=folder).exists()
        )
        self.assertTrue(
            await UserData.objects.filter(
                name="new_file1.txt", owner=TEST_USER, parent=self.private_root
            ).exists()
        )

    @database.transaction(force_rollback=True)
    async def test_download_file(self):
        # test preview file
        file_path = Path(__file__).parent.parent.parent / "pictures/preview.png"
        with file_path.open("rb") as f:
            image = f.read()
        response = self.client.post(
            "resources",
            params={"path": self.private_root.id.hex, "login_require": True},
            files={"files": (file_path.name, image)},
        )
        file = await UserData.objects.get(
            name=file_path.name, owner=TEST_USER, parent=self.private_root
        )
        params = {"path": file.id.hex, "login_require": True}
        for extend_param in ({}, {"preview": True}):
            response = self.client.get("download", params={**params, **extend_param})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.content), len(image))
            self.assertEqual(len(response.content), len(image))
            self.assertEqual(response.headers["Content-Type"], "image/png")
            self.assertEqual(response.headers["Content-Length"], str(len(image)))

        response = self.client.get("download", params={**params, "thumbnail": True})
        return_image = Image.open(BytesIO(response.content))
        self.assertEqual(return_image.size, THUMBNAIL_SIZE)
