Method to use this code:you can use 1 or 2
---------------Method 2
1.find the pgadmin4 to create 2 database: task_db and user_db
2.restore tasks.sql into task_db and users.sql into user_db, you can find the two .sql document in SQL file
3.modify the 2 database.py document in task_service and user_service by using your database name and password:
DATABASE_URL = "postgresql://your database name:your password@localhost:5432/task_db"
4.pip the requirements.txt
And then clink the start.bat document, and input your password for database. Then start the index.html in static.


---------------Method 2
When use this code:
1.find the pgadmin4 to create 2 database: task_db and user_db
2.restore tasks.sql into task_db and users.sql into user_db, you can find the two .sql document in SQL file
3.modify the 2 database.py document in task_service and user_service by using your database name and password:
DATABASE_URL = "postgresql://your database name:your password@localhost:5432/task_db"
4.pip the requirements.txt
5.start task_service in terminal by using: python -m uvicorn task_service.app:app --reload --port 8001
6.start user_service in terminal by using: python -m uvicorn user_service.app:app --reload --port 8000
7.open the task_service\static\index.html
