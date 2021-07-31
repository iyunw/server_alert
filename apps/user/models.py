from django.db import models
from django.contrib.auth.models import AbstractUser  # 引入user模型的基础类
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
    mobile = models.CharField('电话', null=True, blank=True, max_length=15)
    status = models.IntegerField(verbose_name="状态", choices=UserStatus.choices, default=UserStatus.DISABLE)

    # group_alert_server = models.ManyToManyField("alert.GroupAlertServer", verbose_name="报警服务组")

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
