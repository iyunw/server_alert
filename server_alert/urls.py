"""server_alert URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from alert.views import SendMessage, ListBankend, GroupAlertServerModelViewSet, PrometheusSendMessage, SendHistoryViewSet
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from user.views import UserInfo, CustomAuthToken, Register, ActiveUser

route = DefaultRouter()
route.register('server', GroupAlertServerModelViewSet, basename="server")
route.register('logs', SendHistoryViewSet, basename="logs")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/send/prometheus/', PrometheusSendMessage.as_view(), name="send_prometheus"),
    path('api/send/', SendMessage.as_view(), name="send"),
    path('api/bankend/', ListBankend.as_view(), name="bankend"),
    path('api/userinfo/', UserInfo.as_view(), name="userinfo"),
    path('api/register/', Register.as_view(), name="register"),
    path('api/active/', ActiveUser.as_view(), name="active"),
    path('api/', include(route.urls), name="api"),
]
urlpatterns += [
    path('api/api-token-auth/', CustomAuthToken.as_view())
]