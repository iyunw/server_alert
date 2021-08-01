from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from utils.base_alert import send_alert, get_alert_bankend_support
from alert.models import GroupAlertServer, SendHistory, Status
from alert.serializers import GroupAlertServerSerializer, SendHistorySerializer


class ListBankend(APIView):
    def get(self, request, *args, **kwargs):
        resp = get_alert_bankend_support()
        return Response(data=resp, status=HTTP_200_OK)


class BaseSendMessage(APIView):

    def send(self):
        """
        真正发送函数
        :return:
        """
        resp = {}
        for alert_group_id in self.alert_group_ids:
            group_alert_server_obj = GroupAlertServer.objects.filter(id=alert_group_id).first()
            if not group_alert_server_obj or group_alert_server_obj.create_user != self.request.user:
                resp[alert_group_id] = {"status": "FAILE", "alert_server": "none",
                                        "data": {"errmsg": "alert server id is not exits", "code": 403}}
            else:
                resp[alert_group_id] = send_alert(group_alert_server_obj=group_alert_server_obj, data=self.data,
                                                  type=self.alert_type,
                                                  title=self.title)
        SendHistory.objects.create(
            user=self.request.user,
            request_data={
                "alert_group_ids": self.alert_group_ids,
                "title": self.title,
                "data": self.data
            },
            respones_data=resp)
        return resp

    def post(self, request, *args, **kwargs):
        self.request = request
        self.post_data = dict(request.data)
        get_data_except = self.get_data()  # 异常Not Null
        if get_data_except:
            return get_data_except
        resp = self.send()
        return Response(data=resp, status=HTTP_200_OK)

    def get_data(self):
        """
        获取基础数据封装,修改这个方法即可，想办法封装
        :return:
        """
        try:
            self.alert_group_ids = self.post_data.get("alert_group_ids", [])  # list
            self.data = self.post_data.get("data", "")
            self.title = self.post_data.get("title", "机器人")
            self.alert_type = self.post_data.get("type", "text")
        except Exception as e:
            print(e)
            return Response(data={"err": str(e)}, status=HTTP_400_BAD_REQUEST)


class SendMessage(BaseSendMessage):
    """
    发送消息
    """

    def get_data(self):
        """
        获取基础数据封装
        :return:
        """
        try:
            self.alert_group_ids = self.post_data.get("alert_group_ids", [])  # list
            self.data = self.post_data.get("data", "")
            self.title = self.post_data.get("title", "机器人")
            self.alert_type = self.post_data.get("type", "text")
        except Exception as e:
            print(e)
            return Response(data={"err": str(e)}, status=HTTP_400_BAD_REQUEST)


class PrometheusSendMessage(BaseSendMessage):
    """
    Prometheus发送消息接口
    """

    def get_data(self):
        """
        获取基础数据封装
        :return:
        """
        self.alert_group_ids = self.request.query_params.getlist("id")
        print(self.post_data)
        receiver = self.post_data.get("receiver", "")  # 报警组
        count = len(self.post_data["alerts"])
        self.alert_type = self.post_data.get("type", "text")
        self.title = f"[prometheus] [{receiver}]"
        self.data = f"{self.title}\n报警数: {count}\n------\n"
        flag = 1
        for instance in self.post_data["alerts"]:
            alertname = instance["labels"]["alertname"]
            annotations = instance["annotations"]
            instance_data = f"alertname: {alertname}\n"
            for k, v in dict(annotations).items():
                instance_data += f"{k}: {v}\n"

            if flag != len(self.post_data["alerts"]):
                instance_data += f"------\n"
            self.data += instance_data
            flag += 1


class GroupAlertServerModelViewSet(ModelViewSet):
    serializer_class = GroupAlertServerSerializer

    def get_queryset(self):
        resp = GroupAlertServer.objects.filter(create_user=self.request.user).exclude(status=Status.DELETE)
        # print(get_alert_bankend_support())
        return resp

    def perform_create(self, serializer):
        serializer.save(create_user=self.request.user)


class SendHistoryViewSet(ReadOnlyModelViewSet):
    serializer_class = SendHistorySerializer

    def get_queryset(self):
        resp = SendHistory.objects.filter(user=self.request.user)
        return resp
