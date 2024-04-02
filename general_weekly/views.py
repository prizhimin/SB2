from django.shortcuts import render, get_object_or_404, redirect
# from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# from django.utils import timezone
# from django.apps import apps
# from shutil import copy
# import os
# from openpyxl import load_workbook


@login_required
def general_weekly(request):
    return render(request, 'general_weekly/report_list.html')
