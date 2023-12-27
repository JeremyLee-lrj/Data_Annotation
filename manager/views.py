from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


# Create your views here.

def List_Information(request):
    return JsonResponse({
        "name": "Jeremey",
        "age": 23,
    })
