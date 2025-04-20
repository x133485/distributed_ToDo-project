🔥 Task Service 要做的主要内容

模块	具体要做的事情
1. 数据库设计	PostgreSQL 数据库，建一个 tasks 表，字段包括：id, user_id, title, content, created_at, updated_at。
2. FastAPI 搭建服务	类似 User Service，用 FastAPI 写REST接口。
3. CRUD API（四个核心接口）	Create（新增任务）、Read（查询任务）、Update（修改任务）、Delete（删除任务）。
4. 用户验证逻辑	每次API调用时，要先通过发送请求到 User Service，确认用户身份（token 或 user_id）。
5. 错误处理与返回	比如：如果用户不存在，返回错误；如果查不到任务，返回404。
6. 测试接口运行	本地用 Postman 或 curl 测试增删查改是否正常。

7. 制作一个前端进行交互

-----------------------------------
📚 Distributed Note Manager - 用户指南
本项目是一个基于 Python + FastAPI + PostgreSQL 开发的分布式笔记管理系统。
包含用户服务（User Service）与任务服务（Task Service），支持用户注册、登录和任务管理。

✨ 环境准备
1. 安装依赖

在项目根目录下执行：
pip install -r requirements.txt

2.准备数据库
打开 SQL file 文件夹中的初始化 SQL 脚本。

在 pgAdmin 中新建一个数据库（命名 Distributed_Project）。

在新建的数据库里执行 SQL 文件，完成表结构创建。

3.修改配置文件

打开项目中的 config.ini，修改数据库连接信息：
[postgresql]
host = localhost
database = Distributed_Project
user = 你的数据库用户名（默认是postgres，一般不用改）
password = 你的数据库密码
port = 5432（默认端口）
确保 host 和 port 与实际 PostgreSQL 服务器保持一致。

🚀 启动服务
进入到服务的目录下（比如 user_service/，一定要cd进入到app.py所在的文件夹下，不然找不到执行文件），然后运行：

uvicorn app:app --reload --port 8800（在terminal终端执行）
这里 app:app 指的是 app.py 文件中的 FastAPI 实例。

--reload 表示支持热更新，方便开发调试。

--port 8800 指定使用 8800 端口启动服务。（可以使用其他端口，如果修改记得在html文件中也一起修改）


