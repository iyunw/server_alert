from django.db import models
from django.contrib.auth.models import AbstractUser # 引入user模型的基础类
from utils.base_alert import get_alert_bankend
from alert.models import GroupAlertServer


def default_json():
    return {}


class AlertStatus(models.IntegerChoices):
    ENABLE = 0, "开启"
    CLOSE = 1, "关闭"

class UserStatus(models.IntegerChoices):
    ENABLE = 0, "开启"
    DISABLE = 1, "关闭"

class User(AbstractUser):
    cn_name = models.CharField(u'中文名', max_length=30, blank=True)
    mobile = models.CharField('电话', null=True,blank=True,max_length=15)
    status = models.IntegerField(verbose_name="状态", choices=UserStatus.choices, default=UserStatus.DISABLE)
    # group_alert_server = models.ManyToManyField("alert.GroupAlertServer", verbose_name="报警服务组")

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

#
# class UserAlertConfig(models.Model):
#     user = models.ForeignKey("user.User", verbose_name="用户", on_delete=models.CASCADE)
#     type = models.CharField(verbose_name="报警后端类型", choices=get_alert_bankend(), max_length=128)
#     status = models.IntegerField(verbose_name="状态", choices=AlertStatus.choices, default=AlertStatus.ENABLE)
#     create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
#     update_datetime = models.DateTimeField(verbose_name="创建时间", auto_now=True)
#     config = models.JSONField(default=default_json, verbose_name="报警配置")
#     group_alert_server = models.ManyToManyField("alert.GroupAlertServer", verbose_name="报警服务组")
#
#     def __str__(self):
#         return self.user.username
#
#     class Meta:
#         verbose_name = "用户报警信息"
#         verbose_name_plural = verbose_name
