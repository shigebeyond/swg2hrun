#!/usr/bin/python
# https://blog.csdn.net/ccaicjf/article/details/89841534
import requests
import json

# 读文本文件
def read_file(path):
    with open(path, 'r', encoding="utf-8") as file:
        return file.read()

# swagger3自动生成测试用例
class Swagger2hrun:
    # token参数名，也是变量名
    TOKEN_NAME = 'token'

    # 如果url为本地文件，则为测试用
    def __init__(self, url):
        self.url = url

    # 生成用例
    def transform_testcases(self):
        # 请求swagger3 api
        if self.url.startswith('http'):
            swg = requests.get(self.url + '/v3/api-docs').json()
        else: # 测试
            swg = json.loads(read_file(self.url))
            self.url = 'http://localhost'
        self.schemas = swg['components']['schemas']  # 实体类结构描述
        self.tags = list(map(lambda it: it['name'], swg['tags']))  # tag, 对应模块
        self.variables = {} # 记录变量

        tag2cases = {}
        # 遍历paths
        for uri, path in swg['paths'].items():
            # 替换为hrun的变量
            uri = self.fix_uri(uri)

            # 遍历方法： get/post
            for method, api in path.items():
                # 检查过期
                if 'deprecated' in api and api['deprecated']:
                    print(f'接口[{uri}]过期')
                    continue

                # 检查是否存在tag
                tag = api['tags'][0]
                if tag not in self.tags:
                    print(f'接口[{uri}]的tag[{tag}]不存在')
                    continue

                # 处理单个接口(用例)
                testcase = self.parse_api(api, uri, method)

                # 记录
                if tag not in tag2cases:
                    tag2cases[tag] = []
                tag2cases[tag].append(testcase)
        return tag2cases

    # 替换为hrun的变量, 如 user/{userId} 要变为 user/${userId}
    def fix_uri(self, uri):
        if '(' in uri:  # 表达式
            uri = uri.replace('{', '${')
        else:  # 纯变量
            uri.replace('{', '$').replace('}', '')
        return uri

    def parse_api(self, api, uri, method):
        '''
        解析单个api
        :param api: 单个api配置
        :param uri:
        :param method:
        :return:
        '''
        request = {
            "url": uri,
            "method": method.upper(),
            "headers": {},
            "json": {},
            "params": {}
        }
        testcase = {
            "test": {
                "name": api['summary'].replace('/', '_'),
                "variables": {},
                "request": request,
                "validate": [],
                "extract": [],
                "output": []
            }
        }

        # 解析参数
        self.parse_parameters(api, request)
        self.parse_body(api, request)

        # 解析响应
        self.parse_response(api, testcase['test']['validate'])

        # 清理空属性
        for key in ['headers', 'json', 'params']:
            if request[key] == {}:
                del request[key]

        return testcase

    # 解析请求体
    def parse_body(self, api, request):
        if 'requestBody' not in api:
            return

        content = api["requestBody"]["content"]
        content_type = list(content.keys())[0]  # 只有一个 content-type 请求头
        # content-type类型: application/json, application/x-www-form-urlencoded, multipart/form-data
        # https://blog.csdn.net/JackieDYH/article/details/108153797
        is_json = content_type.lower() == "application/json"
        self.parse_schema_params(content[content_type], request, is_json)

    # 解析参数
    def parse_parameters(self, api, request):
        if 'parameters' not in api:
            return

        for param in api['parameters']:
            ''' 处理in
            header: 请求头
            query: 一般urlcode中的“key=value”，也就是相当于@RequestParam标记的参数
            path: get请求url中的“/{userId}” ,也就是相当于@PathVariable标记的参数
            body: 不常用
            form: 不常用    
            '''
            # body 和 query 不会同时出现
            # 1 body
            if param['in'] == 'body':
                self.parse_schema_params(param, request, True)
                continue

            # 2 query
            if param['in'] == 'query':
                name = param['name']
                value = self.get_param_example_value(param, name)
                request['params'].update({name: value})

            # 3 header
            if param['in'] == 'header':
                name = param['name']
                value = self.get_param_example_value(param, name)
                request['headers'].update({name: value})

    # 解析响应
    def parse_response(self, api, validates):
        responses = api['responses']
        if '200' not in responses:
            print("响应描述无200响应码")
            return

        # 获得响应描述
        content = responses['200']['content']['*/*']

        # 获得响应的实体类结构中的属性
        props = self.get_schema_props(content)
        if props == None:
            return

        # 遍历属性来填充校验器
        for name, opt in props.items():
            value = self.get_param_example_value(opt)
            if value != '':
                validate = {
                    'comparator': 'contains',
                    'check': 'content.' + name,
                    'expected': value
                }
                validates.append(validate)

    # 解析实体结构中的参数
    def parse_schema_params(self, param, request, is_json):
        # 获得实体类结构中的属性
        props = self.get_schema_props(param)
        if props == None:
            return

        # testcase.request中的数据字段
        if is_json:
            req_field = 'json'
        else:
            req_field = 'data'

        # 遍历属性来填充参数
        for name, opt in props.items():
            value = self.get_param_example_value(opt, name)
            request[req_field].update({name: value})

    # 获得实体类结构中的属性
    def get_schema_props(self, param):
        if 'schema' not in param or '$ref' not in param['schema']:
            return None

        # 获得实体结构引用的路径，如 #/components/schemas/用户实体
        ref = param['schema']['$ref']
        if not ref:
            return None

        # 实体名，如 用户实体
        name = ref.split('/')[-1]
        # 实体类结构中的属性
        return self.schemas[name]['properties']

    # 获得参数的示例值
    def get_param_example_value(self, value, name=None):
        # 属性值有示例值
        if 'example' in value:
            return value['example']

        # token变量
        if name == self.TOKEN_NAME:
            return '$' + self.TOKEN_NAME

        return ''

    def print_testcases(self, tag2cases):
        print("Swagger3 Api转为 HttpRunner 用例json: ")
        for tag, cases in tag2cases.items():
            for case in cases:
                print("\t" + str(case))

if __name__ == '__main__':
    # hrun = Swagger2hrun('http://localhost:9000')
    hrun = Swagger2hrun('data/swagger-demo.json')
    tag2cases = hrun.transform_testcases()
    hrun.print_testcases(tag2cases)
