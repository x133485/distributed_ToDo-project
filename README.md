🔥 Task Service 要做的主要内容

模块	具体要做的事情
1. 数据库设计	PostgreSQL 数据库，建一个 tasks 表，字段包括：id, user_id, title, content, created_at, updated_at。
2. FastAPI 搭建服务	类似 User Service，用 FastAPI 写REST接口。
3. CRUD API（四个核心接口）	Create（新增任务）、Read（查询任务）、Update（修改任务）、Delete（删除任务）。
4. 用户验证逻辑	每次API调用时，要先通过发送请求到 User Service，确认用户身份（token 或 user_id）。
5. 错误处理与返回	比如：如果用户不存在，返回错误；如果查不到任务，返回404。
6. 测试接口运行	本地用 Postman 或 curl 测试增删查改是否正常。

7. 制作一个前端进行交互
