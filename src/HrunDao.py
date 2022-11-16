import time
import json
from src import Db, Swagger2hrun


# 当前时间字符串
def date():
    times = time.time()
    local_time = time.localtime(times)
    # Y 年 - m 月 - d 日 H 时 - M 分 - S 秒
    return time.strftime("%Y-%m-%d %H:%M:%S", local_time)

class HrunDao:

    def __init__(self, project_name):
        self.project_name = project_name
        self.project_id = None

    # 准备好项目
    def prepare_project(self):
        print("HttpRunnerManager准备项目: " + self.project_name)
        # 检查存在
        item = Db.session.query(Db.ProjectInfo).filter_by(project_name=self.project_name).first()
        if item != None:
            self.project_id = item.id
            return item

        # 若不存在,则插入
        data = Db.ProjectInfo(
            create_time = date(),
            update_time = date(),
            project_name = self.project_name,
            simple_desc = self.project_name,
            responsible_name = '',
            test_user = 'hw',
            dev_user = 'hw',
            publish_app = '',
        )
        Db.session.add(data)
        Db.session.commit()
        self.project_id = data.id
        return data

    # 准备好模块
    def prepare_module(self, name):
        print("HttpRunnerManager准备模块: " + name)
        # 检查存在
        item = Db.session.query(Db.ModuleInfo).filter_by(module_name=name).first()
        if item != None:
            return item

        # 若不存在,则插入
        data = Db.ModuleInfo(
            create_time = date(),
            update_time = date(),
            module_name = name,
            test_user = 'hw',
            simple_desc = name,
            belong_project_id = self.project_id,
        )
        Db.session.add(data)
        Db.session.commit()
        return data

    # 准备好用例
    def save_case(self, case, module_id):
        name = case['test']['name']# 用例名
        print("HttpRunnerManager保存用例: " + name)
        # 检查存在
        item = Db.session.query(Db.TestCaseInfo).filter_by(name=name, belong_module_id=module_id).first()
        if item != None:
            return item

        # 若不存在,则插入
        data = Db.TestCaseInfo(
            create_time = date(),
            update_time = date(),
            type = '1',
            name = name,
            belong_project = self.project_name,
            include = '[]',
            author = 'hw',
            belong_module_id = module_id,
            request = json.dumps(case)
        )
        Db.session.add(data)
        Db.session.commit()
        return data


if __name__ == '__main__':
    # 1 swagger转hrun配置
    tag2cases = json.loads(Swagger2hrun.read_file('data/hrun-demo.json'))
    # 2 存到hrun manager db中
    dao = HrunDao('demo项目')
    # 2.1 项目
    proj = dao.prepare_project()
    for module_name, cases in tag2cases.items():
        # 2.2 模块
        module = dao.prepare_module(module_name)
        # 2.3 用例
        for case in cases:
            dao.save_case(case, module.id)