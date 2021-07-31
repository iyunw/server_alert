from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.authtoken.models import Token
from rest_framework.authtoken import views
from rest_framework.permissions import AllowAny
from user.models import UserStatus, User
from django.core.mail import send_mail
from django.shortcuts import render
from server_alert.settings import BASE_URL, FONT_URL


class CustomAuthToken(views.ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        ret = super(CustomAuthToken, self).post(request, *args, **kwargs)
        token = ret.data["token"]
        if token:
            user_obj = Token.objects.get(key=token).user
            if user_obj.status == UserStatus.DISABLE:
                return Response({"msg": "账号禁用"}, HTTP_400_BAD_REQUEST)
        return ret


class Register(APIView):
    """
    注册
    """
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        data = dict(request.data)
        username = data.get("username", "")
        password = data.get("password", "")
        email = data.get("email", "")
        mobile = data.get("mobile", "")
        if User.objects.filter(username=username).first() or User.objects.filter(email=email).first():
            return Response({"msg": "账号已经注册", "code": 400}, HTTP_400_BAD_REQUEST)
        if username and password and email and mobile:
            user_obj = User.objects.create_user(username=username, password=password, email=email, mobile=mobile)
            token_obj, flag = Token.objects.get_or_create(user=user_obj)
            # todo: send 激活邮件
            resp = send_mail(
                subject='爱运维报警注册',
                message=f'尊敬的{user_obj.username},欢迎注册爱运维报警平台，请点击连接激活您的账号{BASE_URL}/api/active?username={user_obj.username}&token={token_obj.key}',
                from_email=None,
                recipient_list=[user_obj.email],
                fail_silently=False,
            )
            print(resp)
            return Response({"msg": "注册成功，前往邮箱激活", "code": 200}, HTTP_200_OK)
        return Response({"msg": "信息不能为空", "code": 400}, HTTP_400_BAD_REQUEST)


class ActiveUser(APIView):
    """
    激活
    """
    permission_classes = [AllowAny, ]

    def get(self, request, *args, **kwargs):
        url = FONT_URL
        try:
            token = request.GET.get("token", "")
            username = request.GET.get("username", "")
            token_obj = Token.objects.get(key=token)
            user_obj = token_obj.user
            status = "成功"

            if username == token_obj.user.username:
                user_obj.status = UserStatus.ENABLE
                user_obj.save()
                return render(request, "msg.html", locals())
        except:
            status = "失败"
            return render(request, "msg.html", locals())


class UserInfo(APIView):
    """
    获取用户信息
    """

    def get(self, request, *args, **kwargs):
        token = request.GET.get("token", "")
        token_obj = Token.objects.get(key=token)
        user_obj = token_obj.user
        return Response(data={
            "name": user_obj.username,
            "roles": ["admin"],
            "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif"
        }, status=HTTP_200_OK)
