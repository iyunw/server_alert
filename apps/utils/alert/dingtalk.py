import time
import hmac
import hashlib
import base64
import urllib.parse
from utils.base_alert import BaseAlert


class WebHookHandler(BaseAlert):
    @classmethod
    def name(self):
        """
        中文名
        :return:
        """
        return "钉钉群机器人"

    @classmethod
    def support_list(self):
        """
        支持列表
        :return:
        """
        return ["text", "markdown"]

    def __init__(self, group_alert_server_obj):
        super().__init__(group_alert_server_obj)
        self.webhook = group_alert_server_obj.config.get("webhook","")
        self.secret = group_alert_server_obj.config.get("secret","")
        self.timestamp = str(round(time.time() * 1000))
        self.sign = self.get_sign()
        self.url = f"{self.webhook}&timestamp={self.timestamp}&sign={self.sign}"

    def get_sign(self):
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(self.timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return sign

    def send_text(self, data, title=""):
        data = {
            "at": {
                # "atMobiles":[
                #     "180xxxxxx"
                # ],
                # "atUserIds":[
                #     "user123"
                # ],
                # "isAtAll": True
            },
            "text": {
                "content": data
            },
            "msgtype":"text"
        }
        resp = self.request_base(url=self.url, methed="post", data=data)
        return resp

    def send_markdown(self, data, title="钉钉机器人"):
        data = {
             "msgtype": "markdown",
             "markdown": {
                 "title": title,
                 "text": str(data).replace('\n','\n\n')  # todo: 钉钉需要两个\n
             },
              "at": {
                  # "atMobiles": [
                  #     "150XXXXXXXX"
                  # ],
                  # "atUserIds": [
                  #     "user123"
                  # ],
                  # "isAtAll": True
              }
         }
        resp = self.request_base(url=self.url, methed="post", data=data)
        return resp
