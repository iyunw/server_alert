# Generated by Django 3.2.5 on 2021-07-09 00:37

import alert.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0002_auto_20210707_2324'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupAlertServer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='报警组名')),
                ('type', models.CharField(choices=[('sms_ali', 'sms_ali'), ('dingtalk', 'dingtalk'), ('email', 'email')], max_length=128, verbose_name='报警后端类型')),
                ('status', models.IntegerField(choices=[(0, '开启'), (1, '关闭')], default=0, verbose_name='状态')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_datetime', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('config', models.JSONField(default=alert.models.default_json, verbose_name='报警服务端配置')),
            ],
            options={
                'verbose_name': '报警服务器配置',
                'verbose_name_plural': '报警服务器配置',
            },
        ),
        migrations.DeleteModel(
            name='AlertBankend',
        ),
    ]