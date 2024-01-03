import json

from django.http import JsonResponse, QueryDict
from django.shortcuts import render
from datetime import datetime
from common.models import Data, Mission, Expert, Dataset


# Create your views here.

def List(request):
    mission_id = request.GET.get("mission_id")
    mission = Mission.objects.get(mission_id=mission_id)
    mission = mission[0]
    data_all = Data.objects.filter(data_mission_id=mission_id)
    data_all.order_by('data_status')
    dataset = Dataset.objects.filter(dataset_id=mission.mission_dataset_id)
    dataset = dataset[0]
    task_type = dataset.dataset_task_type
    data_source = dataset.dataset_source
    res = []
    for data in data_all:
        if data.data_reserve == 0:  # 不保留的数据过滤掉
            continue
        data_id = data.data_id
        background = data.data_background
        is_labeled = data.data_status
        question = data.data_question
        answer = data.data_answer
        keywords = data.data_keyword
        lastest_time = data.data_lastest_time
        res.append({
            "data_id": data_id,
            "background": background,
            "task_type": task_type,
            "data_source": data_source,
            "is_labeled": is_labeled,
            "question": question,
            "answer": answer,
            "keywords": keywords,
            "lastest_time": lastest_time,
        })
    return JsonResponse({"response": res, "notice": mission.mission_notice})


def label(request):
    put = QueryDict(request.body)
    put_str = list(put.items())[0][0]  # 将获取的QueryDict对象转换为 str 类型
    put_dict = eval(put_str)  # 将str类型转换为字典类型
    data_id = put_dict('data_id')
    data_question = put_dict('data_question')
    data_answer = put_dict('data_answer')
    data_reserve = put_dict('data_reserve')

    data = Data.objects.filter(data_id=data_id)
    data = data[0]
    dataset = Dataset.objects.filter(dataset_id=data.data_dataset_id)
    dataset = dataset[0]
    mission = Mission.objects.filter(mission_id=data.data_mission_id)
    mission = mission[0]
    task_type = dataset.dataset_task_type
    if task_type == "信息补充":
        data.data_question = data_question
        data.data_answer = data_answer
    elif task_type == "质量排序":
        data.data_answer = data_answer
    else:
        data.data_answer = data_answer
        if data.data_answer is None:
            notes = put_dict('notes')
            data.data_answer = json.dumps(notes)
        data.data_reserve = data_reserve
    date_time = datetime.now()
    data.data_lastest_time = '%d/%02d/%2d %02d:%02d:%02d' % (
        date_time.year, date_time.month, date_time.day,
        date_time.hour, date_time.minute, date_time.second
    )
    data.data_status = 1
    mission.mission_data_finished_count += 1
    dataset.dataset_data_finished_count += 1
    data.save()
    mission.save()
    dataset.save()
    return JsonResponse({"response": "success"})