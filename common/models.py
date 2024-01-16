from django.db import models


# Create your models here.

class Manager(models.Model):
    manager_id = models.AutoField(primary_key=True)
    manager_name = models.CharField(max_length=200)
    manager_password = models.CharField(max_length=200)


class Expert(models.Model):
    expert_id = models.AutoField(primary_key=True)
    expert_name = models.CharField(max_length=200)
    expert_password = models.CharField(max_length=200)
    expert_area = models.CharField(max_length=200, null=True)


class Dataset(models.Model):
    dataset_id = models.AutoField(primary_key=True)
    dataset_name = models.CharField(max_length=200)
    dataset_size = models.IntegerField()
    dataset_data_finished_count = models.IntegerField()
    dataset_source = models.CharField(max_length=200, null=True)
    dataset_task_type = models.CharField(max_length=200, null=True)
    dataset_upload_time = models.CharField(max_length=200)
    dataset_assign_time = models.CharField(max_length=200)
    dataset_status = models.IntegerField()  # 0未归档 1已归档


class Data(models.Model):
    data_id = models.AutoField(primary_key=True)
    data_dataset_id = models.IntegerField()
    data_mission_id = models.IntegerField(null=True)
    data_background = models.TextField(null=True)
    data_question = models.TextField(null=True)
    data_answer = models.JSONField(null=True)
    data_status = models.IntegerField()  # 为0表示数据未标注，为1表示已标注
    data_lastest_time = models.CharField(max_length=200)
    data_area = models.TextField(null=True)
    data_keyword = models.TextField(null=True)
    other = models.TextField(null=True)
    data_reserve = models.IntegerField()  # 为0表示不保留，1表示保留


class Mission(models.Model):
    mission_id = models.AutoField(primary_key=True)
    mission_expert_id = models.IntegerField()
    mission_dataset_id = models.IntegerField()
    mission_area = models.CharField(max_length=200, null=True)
    mission_size = models.IntegerField()
    mission_data_finished_count = models.IntegerField()
    mission_create_time = models.CharField(max_length=200)
    mission_due_time = models.CharField(max_length=200)
    mission_notice = models.CharField(max_length=200, null=True)
    mission_original_id = models.IntegerField(null=True)
    mission_transfer = models.IntegerField()  # 为0代表任务未移交，为1代表任务已移交
    mission_highlight = models.IntegerField()  # 为0代表任务未高亮，为1代表任务被管理员催促，需要高亮。


class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    session_username = models.TextField()
    session_usertype = models.TextField()
    session_last_login_year = models.IntegerField(null=True)
    session_last_login_month = models.IntegerField(null=True)
    session_status = models.IntegerField()  # 0代表未登录，1代表已登录
