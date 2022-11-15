import Swagger2hrun
import HrunDao

if __name__ == '__main__':
    # swagger文档的根url, 具体文档为 http://localhost:9000/v3/api-docs
    swagger_url = 'http://localhost:9000'
    # 项目名
    project_name = 'demo项目'

    # 1 swagger转hrun配置
    hrun = Swagger2hrun.Swagger2hrun(swagger_url)
    tag2cases = hrun.transform_testcases()
    hrun.print_testcases(tag2cases)
    # 2 存到hrun manager db中
    dao = HrunDao.HrunDao(project_name)
    # 2.1 项目
    proj = dao.prepare_project()
    for module_name, cases in tag2cases.items():
        # 2.2 模块
        module = dao.prepare_module(module_name)
        # 2.3 用例
        for case in cases:
            dao.save_case(case, module.id)