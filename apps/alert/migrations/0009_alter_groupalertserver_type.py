# Generated by Django 3.2.5 on 2021-07-28 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0008_alter_groupalertserver_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupalertserver',
            name='type',
            field=models.CharField(choices=[('email', 'email'), ('wx_application', 'wx_application'), ('wx_group', 'wx_group'), ('sms_ali', 'sms_ali'), ('dingtalk', 'dingtalk')], max_length=128, verbose_name='报警后端类型'),
        ),
    ]
