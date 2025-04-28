Distributed Task Management System 
---
📚 Project Overview  

This project is a distributed task management system developed for the 2025 Distributed Systems course project.  
It demonstrates the core characteristics of a distributed system, including:  

Microservices architecture  

Network-based communication (REST APIs)  

Remote Procedure Calls (RPC) between services  

Threaded and asynchronous request handling  

Failure detection and resilience  

No shared memory architecture  

Component	Description
---
user_service	Handles user registration, login, and token validation (Port 8000)
task_service	Manages personal and public tasks (Port 8001)
Frontend	Static HTML/JS page interacting with backend via REST API
Databases	Two independent PostgreSQL databases: user_db and task_db

🌐 Key Technologies  
FastAPI — Backend framework  

Uvicorn — ASGI server for asynchronous concurrency  

PostgreSQL — Database storage  

HTTP/REST APIs — Service communication   

RPC — Service-to-service communication (via HTTP)  

CORS — Frontend-backend cross-origin communication  


---

🚀 How to Deploy and Run  
Prerequisites
Python 3.9+
PostgreSQL installed and running
Internet access (for external client testing)

1. Prepare Databases
Create two databases: user_db and task_db

Apply the provided SQL schemas from SQL file/users.sql and SQL file/tasks.sql

2. Install Dependencies  
pip install -r requirements.txt

3. Start Services  
start_all.bat

This script:
Launches user_service on Port 8000
Launches task_service on Port 8001
Automatically opens the static/index.html frontend
Alternatively, you can manually start each service in separate terminals.


5. Client Access
Frontend interacts with backend services over HTTP.
External clients can directly open static/index.html locally.

📜 Design Challenges Addressed  
Network unreliability: Implemented exception handling during RPCs to handle service unavailability.

Node failure resilience: Detects and appropriately responds to service failures.

No shared memory: Each service operates independently with message-passing via HTTP.

Concurrency: Supports multiple simultaneous client interactions using asynchronous threading.

🧪 Core Functionalities  

User registration and login with token generation

Personal task creation, viewing, updating, and deletion

Public task creation with channel codes and channel joining

Token-based authentication for all operations

Failure handling when a dependent service is unavailable
