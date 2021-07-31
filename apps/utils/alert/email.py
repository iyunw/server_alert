import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from utils.base_alert import BaseAlert


class WebHookHandler(BaseAlert):
    @classmethod
    def name(self):
        return "邮件"

    @classmethod
    def support_list(self):
        """
        支持列表
        :return:
        """
        return ["text", "html"]

    def __init__(self, group_alert_server_obj):
        super().__init__(group_alert_server_obj)
        self.group_alert_server_obj = group_alert_server_obj
        self.smtp_host = group_alert_server_obj.config.get("smtp_host", "")
        self.smtp_user = group_alert_server_obj.config.get("smtp_user", "")
        self.smtp_password = group_alert_server_obj.config.get("smtp_password", "")
        self.smtp_sender = group_alert_server_obj.config.get("smtp_sender", "")
        self.smtp_port = group_alert_server_obj.config.get("smtp_port", 465)
        self.smtp_ssl = group_alert_server_obj.config.get("smtp_ssl", True)
        self.receivers = str(self.group_alert_server_obj.config.get("receivers", "")).split(',')

    def send_text(self, data, title=""):
        resp = self._mail(title=title, body=data, type="plain")
        return resp

    def send_markdown(self, data, title="钉钉机器人"):
        resp = self._mail(title=title, body=data, type="html")
        return resp

    def send_html(self, title, data):
        resp = self._mail(title=title, body=data, type="html")
        return resp

    def _mail(self, title, body, type="html"):
        """
        发送邮件基类
        :param title:
        :param body:
        :param type:
        :return:
        """
        try:
            msg = MIMEText(body, type, 'utf-8')
            msg['From'] = formataddr([self.smtp_sender, self.smtp_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            # msg['To'] = formataddr(["myuser", self.receivers])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['To'] = Header(";".join(self.receivers), 'utf-8')
            msg['Subject'] = title  # 邮件的主题，也可以说是标题
            if self.smtp_ssl:
                server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)  # 发件人邮箱中的SMTP服务器，端口是25
            else:
                server = smtplib.SMTP()
                server.connect(self.smtp_host, self.smtp_port)  # 25 为 SMTP 端口号
            server.login(self.smtp_user, self.smtp_password)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(self.smtp_sender, self.receivers, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            print(e)
            return self.request_status("FAILED", {"err": str(e)})
        return self.request_status("OK", {"msg": "发送正常"})
