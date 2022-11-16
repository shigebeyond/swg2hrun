[GitHub](https://github.com/shigebeyond/swg2hrun) | [Gitee](https://gitee.com/shigebeyond/swg2hrun)

# swg2hrun - Swagger3转HttpRunnerManager

## 概述
该库主要用于：
1. Swagger3 Api转为 HttpRunner 用例配置
2. 用例配置存到 HttpRunnerManager 库中

## swg2hrun使用
1. [main.py](main.py) 修改 swagger3 url 等配置
```python
# swagger3文档的根url, 具体文档为 http://localhost:9000/v3/api-docs
swagger_url = 'http://localhost:9000'
# 项目名
project_name = 'demo项目'
```

2. [Db.py](Db.py) 修改 HttpRunnerManager 的数据库连接配置
```
user = 'root'
password = 'test_server_db!'
ip = '192.168.0.182'
port = '3306'
dbname = 'hrun'
```

3.  直接运行[main.py](main.py)

4. 注意:
如果接口有统一的token参数来校验身份或会话, 可以通过修改 `Swagger2hrun.TOKEN_NAME` 来指定这个token参数名, 本库会自动将参数值变为httprunner的变量

## HttpRunnerManager使用
1. HttpRunnerManager db库的新数据
swg2hrun库将 Swagger3 Api 转换为 HttpRunnerManager 中的db对象
```
1 项目名(如"demo项目") => HttpRunnerManager 中的项目
2 Swagger3中的tag => HttpRunnerManager 中的模块
3 Swagger3中的单个接口 => HttpRunnerManager 中的用例
```

2. 添加环境(真实的请求根地址)

3. 配置好变量

4. 运行用例
