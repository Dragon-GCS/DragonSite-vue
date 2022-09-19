# ReadMe

**开发中。。。**

![preview](pictures/preview.png)

## 启动方法

* 前端项目构建： `cd web && npm install && npm build`
* 安装后端依赖：使用`poetry`或[`start`](https://github.com/dragon-gcs/start)自动安装依赖，或根据`pyproject.toml`使用pip手动安装
* 启动服务器：`cd .. && python main.py`, 默认地址：`0.0.0.0:8080`, 也可以用`uvicorn server:app --host <host> --port <port>`启动服务器
* 创建用户：`python manage.py user add <username> <password> --admin`
* 删除用户：`python manage.py user drop 'username'`

## TODO

* docker deploy
