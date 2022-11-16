from sqlalchemy import Column, ForeignKey, String, Integer, FLOAT, DATE, create_engine, desc, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

# 引擎
echo_sql = False
user = 'root'
password = 'test_server_db!'
ip = '192.168.0.182'
port = '3306'
dbname = 'hrun'
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{ip}:{port}/{dbname}?charset=utf8', echo=echo_sql)

# 元数据
metadata = MetaData(engine)

# 创建DBSession类型:
DBSession = sessionmaker(bind=engine, autocommit=False)
session = DBSession()
session.expire_on_commit = False # commit时不过期旧对象, 不然每次commit都会导致大量旧对象重新加载, 反正一个业务方法commit后, 另一个业务方法会重新查询对象, 以便实现方法之间解耦

# 表
tables = {}
# 获得表
def get_table(name):
    if name not in tables:
        tables[name] = Table(name, metadata, autoload=True)

    return tables[name]

# 上一条sql
last_sql = ''

# 插入表
def insert(table_name, values):
    # 连接数据表
    table = get_table(table_name)

    # 构建insert语句
    insert_sql = table.insert()
    # print(insert_sql)

    exec_sql(insert_sql, values)

# 预览sql
def preview_sql(sql, params):
    # 只处理sql是字符串的情况
    if isinstance(sql, str):
        for k, v in params.items():
            if isinstance(v, str):
                v = f"'{v}'"
            elif isinstance(v, datetime.datetime) or isinstance(v, datetime.date):
                v = v.strftime("%Y%m%d")
                v = f"'{v}'"
            sql = sql.replace(':' + k, str(v))

        print(sql)

# 查询sql
def query_sql(sql, params = {}):
    preview_sql(sql, params)
    global last_sql
    last_sql = sql
    cursor = session.execute(sql, params=params)
    return cursor.fetchall()

# 更新sql
def exec_sql(sql, params = {}):
    preview_sql(sql, params)
    global last_sql
    last_sql = sql
    cursor = session.execute(sql, params=params)
    session.commit()
    # print(cursor.lastrowid)

Base = declarative_base()

# 项目信息
class ProjectInfo(Base):
    __tablename__ = 'ProjectInfo'

    id = Column(Integer, primary_key=True)
    project_name = Column(String(50), doc='项目名称', unique=True, nullable=False)
    responsible_name = Column(String(20), doc='负责人', nullable=False)
    test_user = Column(String(100), doc='测试人员', nullable=False)
    dev_user = Column(String(100), doc='开发人员', nullable=False)
    publish_app = Column(String(100), doc='发布应用', nullable=False)
    simple_desc = Column(String(100), doc='简要描述', nullable=True)
    other_desc = Column(String(100), doc='其他信息', nullable=True)
    create_time = Column(DATE, doc='创建时间', nullable=True)
    update_time = Column(DATE, doc='更新时间', nullable=True)

# 模块信息
class ModuleInfo(Base):
    __tablename__ = 'ModuleInfo'

    id = Column(Integer, primary_key=True)
    module_name = Column(String(50), doc='模块名称', nullable=False)
    belong_project_id = Column(Integer)
    test_user = Column(String(50), doc='测试负责人', nullable=False)
    simple_desc = Column(String(100), doc='简要描述', nullable=True)
    other_desc = Column(String(100), doc='其他信息', nullable=True)
    create_time = Column(DATE, doc='创建时间', nullable=True)
    update_time = Column(DATE, doc='更新时间', nullable=True)

# 用例信息
class TestCaseInfo(Base):
    __tablename__ = 'TestCaseInfo'

    id = Column(Integer, primary_key=True)
    type = Column(Integer, doc='test-config', default=1)
    name = Column(String(50), doc='用例-配置名称', nullable=False)
    belong_project = Column(String(50), doc='所属项目', nullable=False)
    belong_module_id = Column(Integer)
    include = Column(String(1024), doc='前置config-test', nullable=True)
    author = Column(String(20), doc='编写人员', nullable=False)
    request = Column(String(20000), doc='请求信息', nullable=False)
    create_time = Column(DATE, doc='创建时间', nullable=True)
    update_time = Column(DATE, doc='更新时间', nullable=True)
