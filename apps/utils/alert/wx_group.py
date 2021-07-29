from utils.base_alert import BaseAlert


class WebHookHandler(BaseAlert):
    @classmethod
    def name(self):
        return "微信群机器人"

    @classmethod
    def support_list(self):
        """
        支持列表
        :return:
        """
        return ["text", "markdown"]

    def __init__(self, group_alert_server_obj):
        super().__init__(group_alert_server_obj)
        self.webhook = group_alert_server_obj.config.get("webhook", "")

    def send_text(self, data, title=""):
        data = {
            "msgtype": "text",
            "text": {
                "content": data,
                # "mentioned_list":["wangqing","@all"],
                # "mentioned_mobile_list":["13800001111","@all"]
            }
        }
        resp = self.request_base(url=self.webhook, methed="post", data=data)
        return resp

    def send_markdown(self, data, title=""):
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": data
            }
        }
        resp = self.request_base(url=self.webhook, methed="post", data=data)
        return resp
