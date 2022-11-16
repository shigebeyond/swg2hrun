[GitHub](https://github.com/shigebeyond/swg2hrun) | [Gitee](https://gitee.com/shigebeyond/swg2hrun)

# swg2hrun - Swagger转HttpRunnerManager

## 概述
该库主要用于：
1. Swagger Api转为 HttpRunner 用例配置，兼容 Swagger v2 与 v3 版本 
2. 用例配置存到 HttpRunnerManager 库中

## swg2hrun使用
1. [main.py](src/main.py) 修改 swagger url 等配置
```python
# swagger文档的url, 必须带v2或v3的字样, 来识别swagger版本
# swagger_url = 'data/swagger-v3-demo.json' # 本地文件
# swagger_url = 'http://localhost:9000/v2/api-docs?group=default' # swagger2
swagger_url = 'http://localhost:9000/v3/api-docs' # swagger3
# 项目名
project_name = 'demo项目'
```

2. [Db.py](src/Db.py) 修改 HttpRunnerManager 的数据库连接配置
```
user = 'root'
password = 'test_server_db!'
ip = '192.168.0.182'
port = '3306'
dbname = 'hrun'
```

3.  直接运行[main.py](src/main.py)

4. 注意:

4.1 如果接口有统一的token参数来校验身份或会话, 可以通过修改 `Swagger2hrun.TOKEN_NAME` 来指定这个token参数名, 本库会自动将参数值变为httprunner的变量

4.2 如果接口都有统一的响应数据结构, 如响应码/错误码等, 则可添加通用的校验器, 参考[main.py](src/main.py)
```
hrun.add_common_validate('status', 200) 
```

## HttpRunnerManager使用
1. HttpRunnerManager db库的新数据:
swg2hrun库将 Swagger Api 转换为 HttpRunnerManager 中的db对象
```
项目名(如"demo项目") => HttpRunnerManager 中的项目
Swagger中的tag => HttpRunnerManager 中的模块
Swagger中的单个接口 => HttpRunnerManager 中的用例
```

2. 添加环境(真实的请求根地址)

3. 配置好变量

4. 运行用例
