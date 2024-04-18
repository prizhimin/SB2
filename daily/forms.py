from django import forms
from commondata.models import Department
from .models import DailyReport, UserDepartment
from django.utils import timezone
from datetime import datetime, timedelta
from .utils import get_date_for_report


# class DateForm(forms.Form):
#    selected_date = forms.DateField(label='Выберите дату')


class DateSelectionForm(forms.Form):
    report_date = forms.DateField(label='Выберите дату сводного отчёта (в формате дд.мм.гггг)',
                                  input_formats=['%d.%m.%Y'])


class DailyReportForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_departments = UserDepartment.objects.filter(user=user)
        department_ids = user_departments.values_list('department__id', flat=True)
        self.fields['department'].queryset = Department.objects.filter(id__in=department_ids).order_by('name')
        self.fields['report_date'].initial = get_date_for_report()

    class Meta:
        model = DailyReport
        fields = ['department', 'report_date', 'field_1', 'field_2', 'field_3', 'field_4', 'field_5', 'field_6',
                  'field_7', 'field_8', 'field_9', 'field_10', 'field_11']
