import os
import abc
import json
import requests
from server_alert.settings import BASE_DIR
from importlib import import_module
from alert.models import GroupAlertServer, Status


def get_alert_bankend_support():
    """
    获取后端支持列表
    :return: banend
    """
    resp = {}
    bankends = get_alert_bankend()
    for bankend in bankends:
        module = import_module("utils.alert." + bankend[0])
        name = module.WebHookHandler.name()
        support_list = module.WebHookHandler.support_list()
        resp[bankend[0]] = {
            "name": name,
            "support_list": support_list
        }

    return resp

def get_alert_bankend():
    """
    获取后端发送支持的列表，使整个系统动态
    :return:
    """
    bankend = set()
    for root, dirs, files in os.walk(os.path.join(BASE_DIR, "apps/utils/alert")):
        # print(root, dirs, files)
        for file in files:
            if not str(file).endswith(".py"):
                continue
            if "__init__" in file:
                continue
            file_name = file.replace(".py", "")
            bankend.add((file_name, file_name))
    # print(bankend)
    return bankend


class BaseAlert(object):
    """
    发送信息基类
    """

    def request_status(self, status, data):
        resp_data = {
            "status": status,
            "data": data
        }
        return resp_data

    def request_base(self, url, methed="get", headers={"Content-Type": "application/json"}, data={}, timeout=10):
        """
        请求基类
        :param url:
        :param methed:
        :param headers:
        :param data:
        :param timeout:
        :return:
        """
        try:
            if methed == "get":
                resp = requests.get(url, timeout=timeout)
            elif methed == "post":
                resp = requests.post(url, headers=headers, data=json.dumps(data), timeout=timeout)
            resp_data = resp.json()
            # print(resp_data)
            return self.request_status("OK", resp_data)
        except Exception as e:
            print(e)
            return self.request_status("FAILED", {"err": str(e)})

    @abc.abstractmethod
    def __init__(self, group_alert_server_obj):
        ...

    @abc.abstractmethod
    def name(self):
        """
        中文名
        :return:
        """
        return "钉钉群机器人"

    @abc.abstractmethod
    def support_list(self):
        """
        支持列表
        :return:
        """
        return ["text", "markdown"]

    @abc.abstractmethod
    def send_text(self, data, title=""):
        ...

    @abc.abstractmethod
    def send_markdown(self, data, title=""):
        ...


class AlertHandler(object):
    """
    报警钩子函数，动态调用后端
    """

    def __new__(mcs, handler_name, group_alert_server_obj, *args, **kwargs):
        try:
            module = import_module(f"utils.alert.{handler_name}")
            return module.WebHookHandler(group_alert_server_obj)
        except ImportError:
            return None


def send_alert(group_alert_server_obj, data, title="我的机器人", type="text"):
    if group_alert_server_obj.status == Status.CLOSE:
        return {
            "alert_server": group_alert_server_obj.name,
            "status": "FAILED",
            "data": {
                "errcode": 20001,
                "errmsg": "报警组关闭"
            }
        }
    alert_obj = AlertHandler(group_alert_server_obj.type, group_alert_server_obj)
    if type == "text":
        resp = alert_obj.send_text(title=title, data=data)
    elif type == "markdown":
        resp = alert_obj.send_markdown(title=title, data=data)
    elif type == "html":
        resp = alert_obj.send_html(title=title, data=data)
    resp["alert_server"] = group_alert_server_obj.name
    return resp


def get_alert_name_support(group_alert_server_id):
    """
    获取别名
    :param group_alert_server_id:
    :return:
    """
    group_alert_server_obj = GroupAlertServer.objects.get(id=group_alert_server_id)
    alert_obj = AlertHandler(group_alert_server_obj.type, group_alert_server_obj)

    name = alert_obj.name()
    support_list = alert_obj.support_list()
    return name,support_list

if __name__ == "__main__":
    bankend = get_alert_bankend_support()
    print(bankend)
