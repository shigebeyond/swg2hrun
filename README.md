[GitHub](https://github.com/shigebeyond/swg2hrun) | [Gitee](https://gitee.com/shigebeyond/swg2hrun)

# swg2hrun - Swagger3转HttpRunnerManager

## 概述
该库主要用于：
1. Swagger3 Api转为 HttpRunner 用例配置
2. 用例配置存到 HttpRunnerManager 库中

##　使用
1. [main.py](main.py) 修改配置
```python
# swagger3文档的根url, 具体文档为 http://localhost:9000/v3/api-docs
swagger_url = 'http://localhost:9000'
# 项目名
project_name = 'demo项目'
```

2. [Db.py](Db.py) 修改数据库连接配置
```
user = 'root'
password = 'test_server_db!'
ip = '192.168.0.182'
port = '3306'
dbname = 'hrun'
```

3.  直接运行[main.py](main.py)