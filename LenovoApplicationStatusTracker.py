import requests
import re
import json
from prettytable import PrettyTable # pip install prettytable
from colorama import Fore, Style, init

cookies = {}

headers = {}

json_data = {
    'projectType': 1,
    'queryType': 1,
}

response = requests.post('https://talent.lenovo.com.cn/gateway/myJob/list', cookies=cookies, headers=headers, json=json_data)
response.encoding = 'utf-8'


init(autoreset=True)


def get_status_text(status_code, result_code):
    status_text = "已完成" if status_code == 1 else "进行中" if status_code == 2 else "未开始"
    result_text = "成功" if result_code == 1 else "失败" if result_code == 2 else "等待结果"
    return status_text, result_text

def highlight_row(status_text, result_text):
    if status_text == "进行中":
        return (Fore.YELLOW + status_text, Fore.YELLOW + result_text)
    else:
        return (status_text, result_text)


def simplify_description(description):
    description_without_tags = re.sub(r"<[^>]+>", "", description)
    description_with_tabs = re.sub(r"(\n|^)(\d+\.)", r"\1\t\2", description_without_tags)
    return description_with_tabs


def parse_job_info(data):
    if data['code'] == 0:
        for job in data['result']:
            # print(Fore.CYAN + f"岗位名称: {job['jobName']}\n")
            # print(Fore.CYAN + "岗位职责:\n\n" + job['jobDuties'].replace("<p>", "").replace("</p>", ""))
            # print(Fore.CYAN + "岗位要求:\n\n" + job['jobRequirement'].replace("<p>", "").replace("</p>", ""))
            print(Fore.CYAN + f"岗位名称: {job['jobName']}\n")
            print(Fore.CYAN + "岗位职责:\n\n" + simplify_description(job['jobDuties']))
            print(Fore.CYAN + "岗位要求:\n\n" + simplify_description(job['jobRequirement']))
            # 创建表格
            table = PrettyTable()
            table.field_names = ["项目", "状态", "结果"]
            
            # 添加节点信息
            node_info = {
                "投递流程": job['nodeVo']['deliveryNodeVo'],
                "考试与评测": job['nodeVo']['examineNodeVo'],
                "面试流程": job['nodeVo']['interviewNodeVo'],
                "录用通知": job['nodeVo']['offerNodeVo']
            }
            
            for node, vo in node_info.items():
                status_text, result_text = get_status_text(vo.get('status'), vo.get('result'))
                highlighted_status, highlighted_result = highlight_row(status_text, result_text)
                table.add_row([node, highlighted_status, highlighted_result])
            
            print(table)
            
parse_job_info(json.loads(response.text))
            node_info = {
                "投递流程": job['nodeVo']['deliveryNodeVo'],
                "考试与评测": job['nodeVo']['examineNodeVo'],
                "面试流程": job['nodeVo']['interviewNodeVo'],
                "录用通知": job['nodeVo']['offerNodeVo']
            }
            
            for node, vo in node_info.items():
                status_text, result_text = get_status_text(vo.get('status'), vo.get('result'))
                highlighted_status, highlighted_result = highlight_row(status_text, result_text)
                table.add_row([node, highlighted_status, highlighted_result])
            
            print(table)


parse_job_info(json.loads(response.text))
