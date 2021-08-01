from rest_framework.serializers import ModelSerializer
from alert.models import GroupAlertServer, SendHistory
from utils.base_alert import get_alert_name_support
from rest_framework import serializers


class GroupAlertServerSerializer(ModelSerializer):
    create_user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    # config = serializers.JSONField(write_only=True)
    class Meta:
        # exclude = ["config"]
        fields = '__all__'
        model = GroupAlertServer

    def to_representation(self, instance):
        ret = super(GroupAlertServerSerializer, self).to_representation(instance)
        ret["type_name"],ret["support_list"] = get_alert_name_support(instance.id)
        ret["status"] = instance.get_status_display()
        return ret


class SendHistorySerializer(ModelSerializer):
    create_datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", input_formats=None)

    class Meta:
        # exclude = ["config"]
        fields = '__all__'
        model = SendHistory

