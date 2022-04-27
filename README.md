# ReadMe

## 运行脚本

* 打包： `cd web && npm build`
* 启动服务器：`cd .. && set FLASK_ENV=development && flask run`
* 创建用户：`flask user add 'username' 'passward' --admin`
* 删除用户：`flask user drop 'username'`
* 数据库：`flask db init; flask db migrate; flask db upgrade`

## API

`/api/disk?querys`

> * logRequire: 0/1 是否需要登录
> * token: 登陆时服务器生成token并发送给客户端存储在cookieStorage或localStorage
> * path: 必须给出的路径

* **GET**
  * `path`: 需要查询的文件夹路径
  * `filter`: all;image;video;document;other 筛选文件种类

* **POST**
  * `path`: 新建资源所在的路径
  * 通过判断`request.file`来确定新建文件还是文件夹
  * `names`: 新建资源的名称列表

* **DELETER** 删除文件或文件夹
  * `isDir`: 删除文件或文件夹
  * `path`: 未给出names时删除path对应的资源
  * `names`: 批量删除path下names中对应的资源

* **PATCH** 重命名文件或文件夹
  * `isDir`:操作对象是否为文件夹，重命名不支持批量操作，移动支持批量操作
  * `target-dir`: 移动的目标路径，仅当names长度不为1时有效
  * `names`: 文件名列表，当长度为1时为重命名，长度大于1时为批量移动，否则移动path至target-dir

`/auth/login` 登陆验证
