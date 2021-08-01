import os
from server_alert.settings import BASE_DIR
from django.db import models


def get_alert_bankend():
    """
    获取后端发送支持的列表，使整个系统动态
    :return:
    """
    bankend = set()
    for root, dirs, files in os.walk(os.path.join(BASE_DIR, "apps/utils/alert")):
        for file in files:
            if not str(file).endswith(".py"):
                continue
            if "__init__" in file:
                continue
            file_name = file.replace(".py", "")
            bankend.add((file_name, file_name))

    return bankend


def default_json():
    return {}


class Status(models.IntegerChoices):
    ENABLE = 0, "开启"
    CLOSE = 1, "关闭"
    DELETE = 9, "删除"


class GroupAlertServer(models.Model):
    name = models.CharField(verbose_name="报警组名", max_length=128)
    type = models.CharField(verbose_name="报警后端类型", choices=get_alert_bankend(), max_length=128)
    status = models.IntegerField(verbose_name="状态", choices=Status.choices, default=Status.ENABLE)
    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_datetime = models.DateTimeField(verbose_name="创建时间", auto_now=True)
    config = models.JSONField(default=default_json, verbose_name="报警服务端配置")
    create_user = models.ForeignKey("user.User", verbose_name="创建用户", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "报警服务器配置"
        verbose_name_plural = verbose_name


class SendHistory(models.Model):
    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    user = models.ForeignKey("user.User", verbose_name="发送用户", on_delete=models.CASCADE)
    request_data = models.JSONField(default=default_json, verbose_name="请求内容")
    respones_data = models.JSONField(default=default_json, verbose_name="请求内容")

    def __str__(self):
        return self.user.cn_name

    class Meta:
        verbose_name = "发送历史内容"
        verbose_name_plural = verbose_name
