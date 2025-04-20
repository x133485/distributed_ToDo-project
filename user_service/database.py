from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import configparser

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')
db_config = config['postgresql']

# 构建数据库URL（SQLAlchemy格式）
SQLALCHEMY_DATABASE_URL = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

# 创建SQLAlchemy引擎和会话
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明基类
Base = declarative_base()