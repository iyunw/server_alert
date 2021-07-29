# Generated by Django 3.2.5 on 2021-07-21 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_useralertconfig_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useralertconfig',
            name='type',
            field=models.CharField(choices=[('wx_group', 'wx_group'), ('wx_application', 'wx_application'), ('dingtalk', 'dingtalk'), ('email', 'email'), ('sms_ali', 'sms_ali')], max_length=128, verbose_name='报警后端类型'),
        ),
    ]
