import json

from django.http import JsonResponse, QueryDict
from django.shortcuts import render
from datetime import datetime
from common.models import Data, Mission, Expert, Dataset


# Create your views here.

def List(request):
    res = []
    usertype = request.session.get("usertype")
    mission = Mission.objects.all()
    if usertype == "expert":
        expert = Expert.objects.filter(expert_name=request.session.get("username"))
        mission = mission.filter(mission_expert_id=expert[0].expert_id)
        for mission_item in mission:
            if mission_item.mission_data_finished_count == mission_item.mission_size:
                continue
            dataset = Dataset.objects.filter(dataset_id=mission_item.mission_dataset_id)
            task_type = dataset[0].dataset_task_type
            mission_data = Data.objects.filter(data_mission_id=mission_item.mission_id)
            if len(mission_data) == 0:
                area = "-"
            else:
                area = mission_data[0].data_area
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
            if mission["is_highlight"] == 1:
                res.append(mission)
        for i in range(len(temp) - 1, -1, -1):
            if temp[i]["status"] != "超时" and temp[i]["is_highlight"] != 1:
                res.append(temp[i])
        return JsonResponse({"response": res})
    elif usertype == "manager":
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
            elif mission_item.mission_finished_count == 0:
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
        if len(mission_data) == 0:
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
    dataset_id = request.POST.get("dataset_id")
    area = request.POST.get("area")
    expert_id_list = request.POST.get("expert_id_list")
    expert_id_list = json.loads(expert_id_list)
    notice = request.POST.get("notice")
    due_time = request.POST.get("due_time")
    n: int = len(expert_id_list)
    data = Data.objects.filter(data_dataset_id=dataset_id, data_area=area)
    tot = len(data)
    m: int = tot % n
    avg: int = int(tot / n)
    i = 0
    data_ptr = 0
    date_time = datetime.now()
    mission_create_time = '%d/%02d/%02d' % (date_time.year, date_time.month, date_time.day)
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
        dataset[0].dataset_assign_time = mission_create_time
        dataset[0].save()
        for _ in range(cnt):
            data[data_ptr].data_mission_id = mission.mission_id
            data[data_ptr].save()
            data_ptr += 1
        i += 1
    return JsonResponse({"response": "success"})


def reassign(request):
    put = QueryDict(request.body)
    put_str = list(put.items())[0][0]  # 将获取的QueryDict对象转换为str 类型
    put_dict = eval(put_str)  # 将str类型转换为字典类型
    mission_id = put_dict.get('mission_id')
    expert_id_list = put_dict.get('expert_id_list')
    expert_id_list = json.loads(expert_id_list)
    mission_notice = put_dict.get('mission_notice')
    mission_due_time = put_dict.get('mission_due_time')
    mission = Mission.objects.filter(mission_id=mission_id)
    mission = mission[0]
    mission.mission_transfer = 1
    tot = mission.mission_size
    finished_tot = mission.mission_data_finished_count
    n = len(expert_id_list)
    tot_m = tot % n
    finished_tot_m = finished_tot % n
    tot_avg = int(tot / n)
    finished_tot_avg = int(finished_tot / n)
    i = 0
    data_ptr = 0
    data = Data.objects.filter(data_mission_id=mission.mission_id)
    data.filter(data_status=0)
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
            data[data_ptr].data_mission_id = new_mission.mission_id
            data[data_ptr].save()
            data_ptr += 1
        i += 1
    return JsonResponse({"response": "success"})


def urgent(request):
    mission_id = request.POST.get("mission_id")
    mission = Mission.objects.filter(mission_id=mission_id)[0]
    mission.mission_highlight = 1
    return JsonResponse({'response': 'success'})
