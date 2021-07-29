# Generated by Django 3.2.5 on 2021-07-21 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0006_auto_20210715_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupalertserver',
            name='status',
            field=models.IntegerField(choices=[(0, '开启'), (1, '关闭'), (9, '删除')], default=0, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='groupalertserver',
            name='type',
            field=models.CharField(choices=[('wx_group', 'wx_group'), ('wx_application', 'wx_application'), ('dingtalk', 'dingtalk'), ('email', 'email'), ('sms_ali', 'sms_ali')], max_length=128, verbose_name='报警后端类型'),
        ),
    ]