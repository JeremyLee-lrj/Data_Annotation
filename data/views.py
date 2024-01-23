import json

from django.http import JsonResponse, QueryDict
from django.shortcuts import render
from datetime import datetime

from common.models import Data, Mission, Expert, Dataset, Session


# Create your views here.

def List(request):
    session_id = request.headers.get("Session-Id")
    session = Session.objects.filter(session_info=session_id)
    if len(session) == 0:
        return JsonResponse({'response': "未登录"})

    session = session[0]
    if session.session_status == 0:
        return JsonResponse({'response': "未登录"})
    if session.session_usertype == 'manager':
        return JsonResponse({'response': "非专家用户"})
    mission_id = request.GET.get("mission_id")
    mission = Mission.objects.filter(mission_id=mission_id)
    mission = mission[0]
    data_all = Data.objects.filter(data_mission_id=mission_id)
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
        temp = res
        res = []
        for item in temp:
            if item["is_labeled"] == 0:
                res.append(item)
        for item in temp:
            if item["is_labeled"] == 1:
                res.append(item)
    return JsonResponse({"response": res, "notice": mission.mission_notice})


def label(request):
    session_id = request.headers.get("Session-Id")
    session = Session.objects.filter(session_info=session_id)
    if len(session) == 0:
        return JsonResponse({'response': "未登录"})

    session = session[0]
    if session.session_status == 0:
        return JsonResponse({'response': "未登录"})
    if session.session_usertype == 'manager':
        return JsonResponse({'response': "专家用户"})
    put_dict = QueryDict(request.body)

    data_id = put_dict.get('data_id')
    data_question = put_dict.get('data_question')
    data_answer = put_dict.get('data_answer')
    data_reserve = put_dict.get('data_reserve')

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
            notes = request.POST.get('notes')
            data.data_answer = json.dumps(notes)
        data.data_reserve = data_reserve
    date_time = datetime.now()
    data.data_lastest_time = '%d/%02d/%02d %02d:%02d:%02d' % (
        date_time.year, date_time.month, date_time.day,
        date_time.hour, date_time.minute, date_time.second
    )
    if data.data_status == 0:
        mission.mission_data_finished_count += 1
        dataset.dataset_data_finished_count += 1
    data.data_status = 1
    data.save()
    mission.save()
    dataset.save()
    return JsonResponse({"response": "success"})
