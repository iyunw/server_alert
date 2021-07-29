# Generated by Django 3.2.5 on 2021-07-13 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0005_alter_groupalertserver_type'),
        ('user', '0005_alter_useralertconfig_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='group_alert_server',
        ),
        migrations.AddField(
            model_name='useralertconfig',
            name='group_alert_server',
            field=models.ManyToManyField(to='alert.GroupAlertServer', verbose_name='报警服务组'),
        ),
        migrations.AlterField(
            model_name='useralertconfig',
            name='type',
            field=models.CharField(choices=[('sms_ali', 'sms_ali'), ('dingtalk', 'dingtalk'), ('wx_group', 'wx_group'), ('wx_application', 'wx_application'), ('email', 'email')], max_length=128, verbose_name='报警后端类型'),
        ),
    ]
