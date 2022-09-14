# NetDisk server

## API

`/api/disk?query`

> * logRequire: 0/1 是否需要登录
> * token: 登陆时服务器生成token并发送给客户端存储在cookieStorage或localStorage
> * path: 必须给出的路径

* **GET**
  * `path`: 需要查询的文件夹路径
  * `filter`: all;image;video;document;other 筛选文件种类

* **POST**
  * `path`: 新建资源所在的路径
  * `is_dir`: 文件夹or文件
  * `names`: 新建资源的名称列表

* **DELETE** 删除文件或文件夹
  * `is_dir`: 删除文件或文件夹
  * `path`: name为空删除path对应的资源
  * `names`: 批量删除path下names中对应的资源

* **PATCH** 重命名文件或文件夹
  * `path`: 进行操作的路径
  * `is_dir`: 仅当未提供`names`时生效。如果是文件夹，则将`path`重命名为`target`, 否则，将`path`移动至`target`
  * `target`: 移动的目标路径，仅当names长度不为1时有效
  * `names`: 未给出时对`path`进行操作，否则对`path`下的文件、文件夹进行移动

`/api/auth/login` 登陆验证

登录流程

1. 第一次登录，后端生成过期时间，保存到cookie， token与用户名保存并返回
2. 前端保存token
3. 每次请求从header中获取token，判断token是否在缓存中
4. 不在缓存则返回401 authentic error
5. 在缓存则验证token是否正确以及是否过期
