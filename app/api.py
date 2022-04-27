from dataclasses import dataclass
from os import path
from typing import List, Union

from flask import Blueprint, request, redirect
from flask_restful import Resource, Api, reqparse, inputs, fields, marshal_with

from app.models import User, UserData, db

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)
parser = reqparse.RequestParser()
parser.add_argument("path", type=inputs.regex(r"^/(\w+/?)+$|/"), required=True)
parser.add_argument("logRequire", type=inputs.boolean)
parser.add_argument("filter", type=str, default="")
parser.add_argument("names", type=inputs.regex(r"^[^/\\,;]+$"), action="append")
parser.add_argument("isDir", type=inputs.boolean)
parser.add_argument("target-dir", type=inputs.regex(r"^/(\w+/?)+$|/"))

resource_fields = {
    "code": fields.String,
    "msg": fields.String,
    "data": fields.Nested({
        "name": fields.String,
        "isDir": fields.Boolean,
        "file_size": fields.Integer,
        "type": fields.String(attribute="mime_type"),
        "owner": fields.String,
        "full_path": fields.String(attribute="real_path"),
        "create_time": fields.DateTime(dt_format='iso8601'),
        "modified_time": fields.DateTime(dt_format='iso8601'),
    }, allow_null=True)
}


@dataclass
class Response:
    code: str = "error"
    msg: str = ""
    data: Union[UserData, List[UserData], None] = None


@api_bp.before_request
def login_require():
    args = parser.parse_args()
    if args["logRequire"]:
        # TODO: check token
        return redirect("/auth/login")


class NetDisk(Resource):
    @marshal_with(resource_fields, envelope='response')
    def get(self):
        """获取目录下的文件列表
        querys:
            path: 目录路径
            filter: 文件名过滤
        """

        args = parser.parse_args()
        print(args)
        owner = None
        content = UserData.query.filter_by(
            real_path=args["path"], mime_type=args["filter"], owner=owner
        ).first()
        if not content:
            return Response(msg=f"No found folder: {args['path']}.")
        return Response(code="sussess",msg=f"Get content: {args['path']}", data=content.children)

    @marshal_with(resource_fields, envelope='response')
    def post(self):
        """新建文件或文件夹
        querys:
            path: 新建资源的所属目录路径
            names: 文件夹或文件名列表
        """

        args = parser.parse_args()
        owner = None
        if request.files:
            pass

        if not args["names"]:
            return Response(msg="No names was given.")
        try:
            args['path'] = args['path'].rstrip("/")  # path = / ==> path = ""
            folders = [UserData.createFolder(args['path'] + "/" + name, owner)[0]
                       for name in args["names"]]
            msg = f"Created {args['names']} in {args['path'] or '/'}"
            db.session.commit()
            return Response(code="sussess", msg=msg, data=folders)
        except ValueError as e:
            return Response(msg=str(e))

    @marshal_with(resource_fields, envelope='response')
    def delete(self):
        """删除指定文件或文件夹
        querys:
            isDir: 是否是文件夹
            path: 要删除的文件或文件夹的路径，未给出names时删除path目录
            names: 如果给出则删除path下names中的文件
        """
        args = parser.parse_args()

        if args["isDir"] is None:
            return Response(msg="No isDir given.")

        try:
            if not args['names']:
                if args["path"] == "/":
                    return Response(msg="Can't delete root folder.")
                data = UserData.dropData(args["path"], args["isDir"], None)[0]
                msg = f"Deleted {data.name} in {path.dirname(data.real_path)}"
            else:
                # path = "/" ==> path = ""
                data = [UserData.dropData(args["path"].rstrip("/") + "/" + name, args["isDir"], None)[0]
                        for name in args["names"]]
                msg = f"Deleted {args['names']} in {args['path'] or '/'}"
            db.session.commit()
            return Response(code="sussess", msg=msg, data=data)
        except ValueError as e:
            return Response(msg=str(e))

    @marshal_with(resource_fields, envelope='response')
    def patch(self):
        """重命名或移动指定文件/文件夹
        querys:
            isDir:操作对象是否为文件夹，重命名不支持批量操作，移动支持批量操作
            target-dir: 目标路径，仅当names长度不为1时有效
            names: 文件名列表，当长度为1时为重命名，长度大于1时为批量移动，未给出则仅移动path至目标目录
        """
        args = parser.parse_args()
        owner = None
        if args["isDir"] is None:
            return Response(msg="No isDir given.")

        args['path'] = args['path'].rstrip("/")  # path = / ==> path = ""
        try:
            print(args)
            # move single file or folder to target
            if not args["names"]:
                if not args["target-dir"]:
                    return Response(msg="Neither names nor target-dir was given.")
                data = UserData.renameData(
                    args["path"], None, args["target-dir"], args["isDir"], owner)[0]
                msg = f"Moved {args['path']} to {args['target-dir']}"
            # Rename and move single file or folder
            elif len(args["names"]) == 1:
                data = UserData.renameData(
                    args["path"], args["names"][0], None, args["isDir"], owner)[0]
                msg = f"Renamed {args['path']} to {data.real_path}"
            # batch rename files or folders
            else:
                data = [UserData.renameData(args["path"] + "/" + name, None, args["target-dir"], args["isDir"], owner)[0]
                        for name in args["names"]]
                msg = f"Batch move {args['names']} in {args['path']} to {args['target-dir']}"
            db.session.commit()
            return Response(code="sussess", msg=msg, data=data)
        except ValueError as e:
            return Response(msg=str(e))


api.add_resource(NetDisk, "/disk")
