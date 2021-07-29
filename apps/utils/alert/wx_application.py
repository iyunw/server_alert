from utils.base_alert import BaseAlert


class WebHookHandler(BaseAlert):
    @classmethod
    def name(self):
        return "微信应用"

    @classmethod
    def support_list(self):
        """
        支持列表
        :return:
        """
        return ["text", "markdown"]

    def __init__(self, group_alert_server_obj):
        super().__init__(group_alert_server_obj)
        self.corpid = group_alert_server_obj.config.get("corpid","")
        self.corpsecret = group_alert_server_obj.config.get("corpsecret","")
        self.agentid = group_alert_server_obj.config.get("agentid","")
        # self.access_token = ""
        # self.url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.access_token}"

    def get_access_token(self):
        access_token = ""
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.corpid}&corpsecret={self.corpsecret}"
        resp = self.request_base(url=url)
        if "err" not in resp:
            try:
                if resp["data"]["errcode"] == 0:
                    access_token = resp["data"]["access_token"]
            except Exception as e:
                print(e)
                return ""
        return access_token

    def send_text(self, data, title=""):
        data = {
           "touser" : "@all",
           # "toparty" : "PartyID1|PartyID2",
           # "totag" : "TagID1 | TagID2",
           "msgtype" : "text",
           "agentid" : self.agentid,
           "text" : {
               "content" : data
           },
           "safe":0,
           "enable_duplicate_check": 0,
           "duplicate_check_interval": 1800
        }
        self.access_token = self.get_access_token()
        self.url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.access_token}"
        resp = self.request_base(url=self.url, methed="post", data=data)
        return resp

    def send_markdown(self, data, title=""):
        data = {
           "touser": "@all",
           # "toparty" : "PartyID1|PartyID2",
           # "totag" : "TagID1 | TagID2",
           "msgtype": "markdown",
           "agentid" : self.agentid,
           "markdown": {
                "content": data
           },
           "enable_duplicate_check": 0,
           "duplicate_check_interval": 1800
        }
        self.access_token = self.get_access_token()
        self.url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.access_token}"
        resp = self.request_base(url=self.url, methed="post", data=data)
        return resp
