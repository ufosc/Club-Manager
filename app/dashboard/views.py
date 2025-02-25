from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import exception_handler

# Create your views here.

def index(request):
    context = {}

    return render(request, "dashboard/dashboard_base.html", context)
