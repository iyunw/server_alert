from utils.base_alert import BaseAlert
from user.models import AlertStatus
from typing import List
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
            access_key_id: str,
            access_key_secret: str,
    ) -> Dysmsapi20170525Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 您的AccessKey ID,
            access_key_id=access_key_id,
            # 您的AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = 'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)

    @staticmethod
    def main(
            accessKeyId: str,
            accessKeySecret: str,
            phones: str,
            sign_name: str,
            template_code: str,
            template_param: str,  # json
            args: List[str],
    ) -> object:
        client = Sample.create_client(accessKeyId, accessKeySecret)
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=phones,
            sign_name=sign_name,
            template_code=template_code,
            template_param=template_param
        )
        # 复制代码运行请自行打印 API 的返回值
        resp = client.send_sms(send_sms_request)
        print(resp)
        return resp


class WebHookHandler(BaseAlert):
    @classmethod
    def name(self):
        return "阿里短信"

    @classmethod
    def support_list(self):
        """
        支持列表
        :return:
        """
        return ["text"]

    def __init__(self, group_alert_server_obj):
        super().__init__(group_alert_server_obj)
        self.group_alert_server_obj = group_alert_server_obj
        self.accessKeyId = group_alert_server_obj.config.get("accessKeyId", "")
        self.accessKeySecret = group_alert_server_obj.config.get("accessKeySecret", "")
        self.sign_name = group_alert_server_obj.config.get("sign_name", "")
        self.template_code = group_alert_server_obj.config.get("template_code", "")
        self.phones = group_alert_server_obj.config.get("phones", [])

    def send_text(self, data, title=""):
        resp = Sample.main(accessKeyId=self.accessKeyId, accessKeySecret=self.accessKeySecret, sign_name=self.sign_name,
                           template_code=self.template_code, template_param=str(data))
        return resp

    def send_markdown(self, data, title="钉钉机器人"):
        resp = Sample.main(accessKeyId=self.accessKeyId, accessKeySecret=self.accessKeySecret, sign_name=self.sign_name,
                           template_code=self.template_code, template_param=str(data))
        return resp
