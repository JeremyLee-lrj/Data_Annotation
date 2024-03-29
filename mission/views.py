import json

from django.http import JsonResponse, QueryDict
from django.shortcuts import render
from datetime import datetime
from common.models import Data, Mission, Expert, Dataset, Session


# Create your views here.

def List(request):
    res = []
    session_id = request.headers.get("Session-Id")
    session = Session.objects.filter(session_info=session_id)
    if session.count() == 0:
        return JsonResponse({'response': "未登录"})

    session = session[0]
    if session.session_status == 0:
        return JsonResponse({'response': "未登录"})
    usertype = session.session_usertype
    mission = Mission.objects.all()
    if usertype == "expert":
        expert = Expert.objects.filter(expert_name=session.session_username)
        mission = mission.filter(mission_expert_id=expert[0].expert_id, mission_transfer=0)
        for mission_item in mission:
            if mission_item.mission_data_finished_count == mission_item.mission_size:
                continue
            dataset = Dataset.objects.filter(dataset_id=mission_item.mission_dataset_id)
            task_type = dataset[0].dataset_task_type
            # mission_data = Data.objects.filter(data_mission_id=mission_item.mission_id)
            # if len(mission_data) == 0:
            #     area = "-"
            # else:
            #     area = mission_data[0].data_area
            if mission_item.mission_size == 0:
                area = "-"
            else:
                area = mission_item.mission_area
            resource = dataset[0].dataset_source
            assign_time = mission_item.mission_create_time
            due_time = mission_item.mission_due_time
            date = datetime.now()
            now = [date.year, date.month, date.day]
            due_year = int(due_time[0:4])
            due_month = int(due_time[5:7])
            due_day = int(due_time[8:10])
            due = [due_year, due_month, due_day]
            finished_count = mission_item.mission_data_finished_count
            total_count = mission_item.mission_size
            is_highlight = mission_item.mission_highlight
            if due < now:
                status = "超时"
            elif mission_item.mission_data_finished_count == 0:
                status = "未开始"
            else:
                status = "未完成"
            res.append({
                "task_id": mission_item.mission_id,
                "task_type": task_type,
                "area": area,
                "resource": resource,
                "assign_time": assign_time,
                "due_time": due_time,
                "status": status,
                "finished_count": finished_count,
                "total_count": total_count,
                "is_highlight": is_highlight,
            })
        temp = res
        res = []
        for mission in temp:
            if mission["status"] == "超时":
                res.append(mission)
        for mission in temp:
            if mission["status"] == "超时":
                continue
            if mission["is_highlight"] == 1:
                res.append(mission)
        for i in range(len(temp) - 1, -1, -1):
            if temp[i]["status"] != "超时" and temp[i]["is_highlight"] != 1:
                res.append(temp[i])
        return JsonResponse({"response": res})
    elif usertype == "manager":
        mission = mission.filter(mission_transfer=0)
        for mission_item in mission:
            if mission_item.mission_data_finished_count == mission_item.mission_size:
                continue
            dataset = Dataset.objects.filter(dataset_id=mission_item.mission_dataset_id)
            dataset_name = dataset[0].dataset_name
            task_type = dataset[0].dataset_task_type
            expert = Expert.objects.filter(expert_id=mission_item.mission_expert_id)
            expert_name = expert[0].expert_name
            assign_time = mission_item.mission_create_time
            due_time = mission_item.mission_due_time
            date = datetime.now()
            now = [date.year, date.month, date.day]
            due_year = int(due_time[0:4])
            due_month = int(due_time[5:7])
            due_day = int(due_time[8:10])
            due = [due_year, due_month, due_day]
            finished_count = mission_item.mission_data_finished_count
            total_count = mission_item.mission_size
            is_highlight = mission_item.mission_highlight
            if due < now:
                status = "超时"
            elif mission_item.mission_data_finished_count == 0:
                status = "已分配"
            else:
                status = "标注中"
            res.append({
                "task_id": mission_item.mission_id,
                "task_type": task_type,
                "expert_name": expert_name,
                "dataset_name": dataset_name,
                "status": status,
                "assign_time": assign_time,
                "due_time": due_time,
                "finished_count": finished_count,
                "total_count": total_count,
                "is_highlight": is_highlight,
            })
        temp = res
        res = []
        for i in range(len(temp) - 1, -1, -1):
            res.append(temp[i])
        return JsonResponse({"response": res})
    else:
        return JsonResponse({"response": "请先登录"})


def list_by_dataset(request):
    """
    获取指定数据集的标注任务列表
    :param request:
    :return:
    """
    session_id = request.headers.get("Session-Id")
    session = Session.objects.filter(session_info=session_id)
    if session.count() == 0:
        return JsonResponse({'response': "未登录"})

    session = session[0]
    if session.session_status == 0:
        return JsonResponse({'response': "未登录"})
    if session.session_usertype == 'expert':
        return JsonResponse({'response': "非管理员用户"})
    dataset_id = request.GET.get('dataset_id')
    res = []
    dataset = Dataset.objects.filter(dataset_id=dataset_id)[0]
    missions = Mission.objects.filter(mission_dataset_id=dataset.dataset_id)
    for mission in missions:
        mission_id = mission.mission_id
        expert = Expert.objects.filter(expert_id=mission.mission_expert_id)
        expert_name = expert[0].expert_name
        dataset = Dataset.objects.filter(dataset_id=mission.mission_dataset_id)
        mission_data = Data.objects.filter(data_mission_id=mission_id)
        if mission_data.count() == 0:
            area = "-"
        else:
            area = mission_data[0].data_area
        finished_count = mission.mission_data_finished_count
        total_count = mission.mission_size
        assign_time = mission.mission_create_time
        if mission.mission_transfer == 1:
            status = "已移交"
        elif mission.mission_data_finished_count == mission.mission_size:
            status = "已完成"
        else:
            status = "标注中"
        original_id = mission.mission_original_id
        if original_id == -1:
            original_id = "-"
        else:
            original_id = str(original_id)
        res.append({
            "mission_id": mission_id,
            "expert_name": expert_name,
            "area": area,
            "dataset_name": dataset[0].dataset_name,
            "status": status,
            "original_id": original_id,
            "assign_time": assign_time,
            "finished_count": finished_count,
            "total_count": total_count,
        })
    return JsonResponse({"response": res})


def assign(request):
    print("----Get data from fron-end----")
    session_id = request.headers.get("Session-Id")
    session = Session.objects.filter(session_info=session_id)
    if session.count() == 0:
        return JsonResponse({'response': "未登录"})

    session = session[0]
    if session.session_status == 0:
        return JsonResponse({'response': "未登录"})
    if session.session_usertype == 'expert':
        return JsonResponse({'response': "非管理员用户"})

    print("----Verify user authentication finished----")
    dataset_id = request.POST.get("dataset_id")
    area = request.POST.get("area")
    expert_id_list = request.POST.get("expert_id_list")
    expert_id_list = json.loads(expert_id_list)
    notice = request.POST.get("notice")
    due_time = request.POST.get("due_time")
    n: int = len(expert_id_list)
    data = Data.objects.filter(data_dataset_id=dataset_id, data_area=area)
    tot = data.count()
    m: int = tot % n
    avg: int = int(tot / n)
    i = 0
    data_ptr = 0
    date_time = datetime.now()
    mission_create_time = '%d/%02d/%02d' % (date_time.year, date_time.month, date_time.day)
    print("----pre process finished----")
    for expert_id in expert_id_list:
        cnt = avg
        if i < m:
            cnt += 1
        mission = Mission(
            mission_expert_id=expert_id,
            mission_dataset_id=dataset_id,
            mission_area=area,
            mission_size=cnt,
            mission_data_finished_count=0,
            mission_create_time=mission_create_time,
            mission_due_time=due_time,
            mission_notice=notice,
            mission_original_id=-1,
            mission_transfer=0,
            mission_highlight=0,
        )
        mission.save()
        dataset = Dataset.objects.filter(dataset_id=dataset_id)
        dataset = dataset[0]
        dataset.dataset_assign_time = mission_create_time
        dataset.save()

        print("-----Action before data finish------")
        for _ in range(cnt):
            data[data_ptr].data_mission_id = mission.mission_id
            data[data_ptr].save()
            data_ptr += 1
        i += 1
    return JsonResponse({"response": "success"})


def reassign(request):
    session_id = request.headers.get("Session-Id")
    session = Session.objects.filter(session_info=session_id)
    if session.count() == 0:
        return JsonResponse({'response': "未登录"})

    session = session[0]
    if session.session_status == 0:
        return JsonResponse({'response': "未登录"})
    if session.session_usertype == 'expert':
        return JsonResponse({'response': "非管理员用户"})
    put_dict = QueryDict(request.body)

    mission_id = put_dict.get('mission_id')
    expert_id_list = put_dict.get('expert_id_list')
    expert_id_list = json.loads(expert_id_list)
    mission_notice = put_dict.get('mission_notice')
    mission_due_time = put_dict.get('mission_due_time')
    mission = Mission.objects.filter(mission_id=mission_id)
    mission = mission[0]
    mission.mission_transfer = 1
    mission.save()
    tot = mission.mission_size
    finished_tot = mission.mission_data_finished_count
    n = len(expert_id_list)
    tot_m = tot % n
    finished_tot_m = finished_tot % n
    tot_avg = int(tot / n)
    finished_tot_avg = int(finished_tot / n)
    i = 0
    data_ptr = 0
    data = Data.objects.filter(data_mission_id=mission.mission_id, data_status=0)
    # print("tot cnt:\n", len(data))
    for expert_id in expert_id_list:
        finished_tot_cnt = finished_tot_avg
        tot_cnt = tot_avg
        if i < tot_m:
            tot_cnt += 1
        if i < finished_tot_m:
            finished_tot_cnt += 1
        new_mission = Mission(
            mission_expert_id=expert_id,
            mission_dataset_id=mission.mission_dataset_id,
            mission_area=mission.mission_area,
            mission_size=tot_cnt,
            mission_data_finished_count=finished_tot_cnt,
            mission_create_time=mission.mission_create_time,
            mission_due_time=mission_due_time,
            mission_notice=mission_notice,
            mission_original_id=mission.mission_id,
            mission_transfer=0,
            mission_highlight=0,
        )
        new_mission.save()
        for _ in range(tot_cnt - finished_tot_cnt):
            data_now = data[data_ptr]
            data_now.data_mission_id = new_mission.mission_id
            # print(data_now.data_mission_id)
            data_now.save()
            data_ptr += 1
        i += 1
    return JsonResponse({"response": "success"})


def urgent(request):
    session_id = request.headers.get("Session-Id")
    session = Session.objects.filter(session_info=session_id)
    if session.count() == 0:
        return JsonResponse({'response': "未登录"})

    session = session[0]
    if session.session_status == 0:
        return JsonResponse({'response': "未登录"})
    if session.session_usertype == 'expert':
        return JsonResponse({'response': "非管理员用户"})
    mission_id = request.POST.get("mission_id")
    mission = Mission.objects.filter(mission_id=mission_id)[0]
    mission.mission_highlight = 1
    mission.save()
    return JsonResponse({'response': 'success'})
