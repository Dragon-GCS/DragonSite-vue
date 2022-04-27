from datetime import datetime
from hashlib import md5
from os import path
from typing import List, Tuple, cast, Optional

from flask_sqlalchemy import SQLAlchemy
from app.typing.sql_alchemy import SQLAlchemyStub

# avoid pylance warning,refer: https://github.com/microsoft/pylance-release/issues/187
# https://github.com/WilsonPhooYK/udemy-automated-software-testing-python/tree/main/section6_7/typings
db = cast(SQLAlchemyStub, SQLAlchemy())
Model = db.Model


def getRealPath(name: str, parent_path: Optional[str]) -> str:
    """Concat parent's real_path and name to get real path."""

    name = name.replace("/", "")
    if parent_path is None:
        return "/"
    if parent_path == "/":
        return parent_path + name
    return parent_path + "/" + name


class User(Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column("用户名", db.String(80), unique=True)
    password = db.Column("密码", db.String(32))
    isAdmin = db.Column("管理员权限", db.Boolean)

    data = db.relationship("UserData", backref="owner_obj",
                           lazy="dynamic", cascade="all")

    def __init__(self, username: str, password: str, isAdmin: bool = False) -> None:
        self.username = username
        self.set_password(password)
        self.isAdmin = isAdmin

    def __repr__(self):
        return f"User: {self.username}" + (" <admin>" if self.isAdmin else "")

    def validate_password(self, password: str) -> bool:
        return md5(password.encode("utf-8")).hexdigest() == self.password

    def set_password(self, password: str) -> None:
        self.password = md5(password.encode("utf-8")).hexdigest()

    @classmethod
    def add_user(cls, username: str, password: str, isAdmin: bool = False) -> "User":
        admin = User.query.filter_by(isAdmin=True).first()
        if isAdmin and admin:
            exit(f"Only one admin<{admin.username}> user allowed.")
        user = cls(username, password, isAdmin)
        UserData.initRoot(user)
        db.session.add(user)
        db.session.commit()
        return user


class UserData(Model):
    __tablename__ = "user_data"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("名称", db.String(80))
    real_path = db.Column("路径全称", db.String(2048))
    mime_type = db.Column("文件类型", db.String(80))
    create_time = db.Column("创建时间", db.DateTime, default=datetime.now)
    modified_time = db.Column("修改时间", db.DateTime, default=datetime.now)
    file_size = db.Column("文件大小", db.Integer)
    isDir = db.Column("是否为文件夹", db.Boolean)

    digest = db.Column(db.String(32), db.ForeignKey("digests.digest"))
    owner = db.Column(db.Integer, db.ForeignKey("users.用户名"))
    parent_id = db.Column(db.Integer, db.ForeignKey(
        "user_data.id", ondelete="CASCADE"))
    parent = db.relationship(
        "UserData", backref="children", remote_side=[id])
    children: List["UserData"]

    def __init__(
        self,
        real_path: str,
        mime_type: str,
        file_size: int,
        isDir: bool,
        digest_obj: Optional["Digest"],
        owner_obj: Optional["User"],
    ) -> None:
        print(real_path)
        # check if the parent folder exists
        parent = UserData.query.filter_by(
            real_path=path.dirname(real_path), owner=owner_obj
        ).first()
        if not parent and real_path != "/":
            raise ValueError(
                f"Parent folder({path.dirname(real_path)}) of {real_path} not found.")

        self.name = path.basename(real_path)
        self.real_path = real_path
        self.mime_type = mime_type
        self.file_size = file_size
        self.isDir = isDir
        self.digest_obj = digest_obj
        self.owner_obj = owner_obj
        self.parent = parent if real_path != "/" else None

    def delete(self) -> SQLAlchemyStub:
        """Delete this data and all its children."""

        for child in self.children:
            child.delete()
        db.session.delete(self)
        return db

    def rename(self, new_name: Optional[str], parent_path: Optional[str]) -> Tuple["UserData", SQLAlchemyStub]:
        """Rename or remove the file or folder 
        if new_name was given, rename this item,
        if parent_path was given, remove this item."""

        if not new_name and not parent_path:
            raise ValueError(
                "Check that new_name or target-path was given correctly.")
        # remove this file or folder
        if parent_path:
            parent = UserData.query.filter_by(
                real_path=parent_path, owner=self.owner, isDir=True
            ).first()
            if not parent:
                raise ValueError(f"Parent folder({parent_path}) not found.")
            self.parent = parent
            # rstrip("/"): parent_path = "/" => parent_path = ""
            self.real_path = parent_path.rstrip("/") + "/" + self.name
        # rename this file or folder
        if new_name:
            self.name = new_name
            self.real_path = path.dirname(
                self.real_path).rstrip("/") + "/" + new_name
        if UserData.query.filter_by(real_path=self.real_path, owner=self.owner).first():
            raise ValueError(f"{self.real_path} already exists.")
        # apply changes on all children
        self.modified_time = datetime.now()
        for child in self.children:
            child.rename(child.name, self.real_path)
        return self, db

    @classmethod
    def createFolder(
        cls, real_path: str, owner: Optional["User"],
    ) -> Tuple["UserData", SQLAlchemyStub]:
        """Create a folder record in database by given real_path and owner."""

        folder = UserData.query.filter_by(
            real_path=real_path, owner_obj=owner, isDir=True
        ).first()
        if not folder:
            folder = UserData(
                real_path=real_path,
                file_size=0,
                isDir=True,
                digest_obj=None,
                mime_type="",
                owner_obj=owner,
            )
            db.session.add(folder)
        return folder, db

    @classmethod
    def createFile(
        cls, real_path: str, mime_type: str, digest_obj: "Digest", owner: Optional["User"], file_size: int = 0
    ) -> Tuple["UserData", SQLAlchemyStub]:
        """Create a file with the given name, parent_folder, mime_type, digest_obj, owner and file_size."""

        file = UserData.query.filter_by(
            real_path=real_path, owner_obj=owner, isDir=False
        ).first()
        if not file:
            file = UserData(
                real_path=real_path,
                file_size=file_size,
                isDir=False,
                digest_obj=digest_obj,
                mime_type=mime_type,
                owner_obj=owner,
            )
            db.session.add(file)
        return file, db

    @classmethod
    def initRoot(cls, owner: Optional["User"]) -> "UserData":
        """Initialize the root folder of the given user."""

        root, db = cls.createFolder(real_path="/", owner=owner)
        db.session.commit()
        return root

    @classmethod
    def dropData(
        cls, real_path: str, isDir: bool, owner: Optional["User"]
    ) -> Tuple["UserData", SQLAlchemyStub]:
        """Drop the data with the given real_path, isDir and owner."""

        data = UserData.query.filter_by(
            real_path=real_path, owner_obj=owner, isDir=isDir
        ).first()
        if not data:
            raise ValueError(f"{real_path} not found.")
        data.delete()
        return data, db

    def __repr__(self):
        return f"{'Folder' if self.isDir else 'File'}: {self.real_path} <Owner: {self.owner}>"

    @classmethod
    def renameData(
        cls, real_path: str, new_name: Optional[str], target_dir: Optional[str], isDir: bool, owner: Optional["User"]
    ) -> Tuple["UserData", SQLAlchemyStub]:
        """Move the data with the given real_path, target_dir and owner."""

        data = UserData.query.filter_by(
            real_path=real_path, owner_obj=owner, isDir=isDir
        ).first()
        if not data:
            raise ValueError(f"{real_path} not found.")
        data.rename(new_name, target_dir)
        return data, db


class Digest(Model):
    __tablename__ = "digests"
    digest = db.Column("digest", db.String(32), primary_key=True)
    files: List[UserData] = db.relationship("UserData", backref="digest_obj")

    def __init__(self, digest: str) -> None:
        self.digest = digest

    def cheak_files(self) -> bool:
        return bool(self.files)
