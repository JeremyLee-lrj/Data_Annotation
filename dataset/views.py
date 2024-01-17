import json
from datetime import datetime

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render

from common.models import Data, Mission, Expert, Dataset


# Create your views here.

def get_dataset(request):
    dataset_id = request.GET.get('dataset_id')
    data = Data.objects.filter(data_dataset_id=dataset_id).values('data_area', 'data_mission_id').annotate(
        data_count=Count('data_id'))
    # data1 = Data.objects.filter(data_dataset_id=dataset_id).values('data_area', 'data_mission_id')
    # print(data1)
    # print(data1.annotate(data_count=Count('data_id')))
    # print(data)
    res = []
    for data_single in data:
        mission_id = data_single["data_mission_id"]
        dataset_size = Dataset.objects.filter(dataset_id=dataset_id)[0].dataset_size
        if mission_id is not None:
            expert_id = Mission.objects.filter(mission_id=mission_id)[0].mission_expert_id
            expert_name = Expert.objects.filter(expert_id=expert_id)[0].expert_name
        else:
            expert_name = '-'
        is_assigned = True
        if expert_name == '-':
            is_assigned = False
        data_size = data_single["data_count"]
        area = data_single["data_area"]
        res.append({
            "area": area,
            "data_size": data_size,
            "dataset_size": dataset_size,
            "is_assigned": is_assigned,
            "expert_name": expert_name
        })
    return JsonResponse({"response": res})


def list_dataset(request):
    dataset = Dataset.objects.filter(dataset_status=0)
    res = []
    for data in dataset:
        dataset_id = data.dataset_id
        dataset_name = data.dataset_name
        dataset_task_type = data.dataset_task_type
        dataset_source = data.dataset_source
        dataset_upload_time = data.dataset_upload_time
        dataset_assign_time = data.dataset_assign_time
        exist = False
        for mission in Mission.objects.all():
            if (mission.mission_dataset_id == dataset_id) and (
                    mission.mission_data_finished_count < mission.mission_size):
                exist = True

        if data.dataset_assign_time == "-/-/-":
            status = "未分配"
        elif data.dataset_data_finished_count == data.dataset_size:
            status = "已结束"
        elif exist:
            status = "已分配"
        else:
            status = "已完成"
        res.append({
            "dataset_id": dataset_id,
            "dataset_name": dataset_name,
            "dataset_task_type": dataset_task_type,
            "dataset_source": dataset_source,
            "dataset_upload_time": dataset_upload_time,
            "dataset_assign_time": dataset_assign_time,
            "status": status
        })
    temp = res
    res = []
    for i in range(len(temp) - 1, -1, -1):
        res.append(temp[i])
    return JsonResponse({"response": res})


# 从前端接收到上传的数据集数据，在Dataset表中创建数据集，在Data表中创建数据
# Hopefully, dataset_json which is from front-end should look like as follows
# '''
#    [
#       {
#           "data_background":"xxx",
#           "data_question":"xxx",
#           "data_answer":Json,
#           "data_area":"xxx",
#           "data_keyword":"xxx",
#           "other":"xxx"
#       }
#       ...
#    ]
# '''
def upload_dataset(request):
    data = request.POST
    dataset_name = data.get("dataset_name")
    dataset_task_type = data.get("dataset_task_type")
    dataset_source = data.get("dataset_source")
    dataset_json = data.get("dataset_json")
    data_list = json.loads(dataset_json)
    dataset_status = 0
    dataset_data_finished_count = 0
    dataset_size = len(data_list)
    date_time = datetime.now()
    dataset_upload_time = '%d/%02d/%02d' % (date_time.year, date_time.month, date_time.day)
    dataset = Dataset(
        dataset_name=dataset_name,
        dataset_size=dataset_size,
        dataset_data_finished_count=dataset_data_finished_count,
        dataset_task_type=dataset_task_type,
        dataset_source=dataset_source,
        dataset_upload_time=dataset_upload_time,
        dataset_assign_time="-/-/-",
        dataset_status=dataset_status
    )
    dataset.save()
    for data_item in data_list:
        data = Data(
            data_dataset_id=dataset.dataset_id,
            data_background=data_item["data_background"],
            data_question=data_item["data_question"],
            data_answer=data_item["data_answer"],
            data_status=0,
            data_lastest_time="-/-/-",
            data_area=data_item["data_area"],
            data_keyword=data_item["data_keyword"],
            other=data_item["other"],
            data_reserve=1,
        )
        res = []
        i = 0
        for ans in data.data_answer:
            res.append({
                "answer": ans,
                "ranking_number": i,
                "reserve": 1,
            })
            i = i + 1
        data.data_answer = json.dumps(res)
        data.save()
    return JsonResponse({"response": "success"})


def download_dataset(request):
    dataset_id = request.GET.get("dataset_id")
    dataset = Dataset.objects.filter(dataset_id=dataset_id)[0]
    data_list = Data.objects.filter(data_dataset_id=dataset_id).filter(data_reserve=1)
    dataset.dataset_status = 1
    res = []
    for data in data_list:
        mission_id = data.data_mission_id
        expert_id = Mission.objects.filter(mission_id=mission_id)[0].mission_expert_id
        expert_name = Expert.objects.filter(expert_id=expert_id)[0].expert_name
        res.append({
            "data_background": data.data_background,
            "data_question": data.data_question,
            "data_answer": data.data_answer,
            "data_area": data.data_area,
            "data_keyword": data.data_keyword,
            "other": data.other,
            "expert_name": expert_name,
        })
    return JsonResponse({"response": res})
