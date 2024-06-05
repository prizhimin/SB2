from datetime import datetime
from django import forms
from commondata.models import Department
from .models import WeeklyReport, WeeklyUserDepartment
from .utils import friday_of_week


class WeeklyReportForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_departments = WeeklyUserDepartment.objects.filter(user=user)
        department_ids = user_departments.values_list('department__id', flat=True)
        self.fields['report_date'].input_formats = ['%d.%m.%Y']
        self.fields['department'].queryset = Department.objects.filter(id__in=department_ids).order_by('name')
        self.fields['report_date'].initial = friday_of_week(datetime.now())

    class Meta:
        model = WeeklyReport
        fields = ['department', 'report_date', 'field1', 'field2', 'field3', 'field4', 'field5', 'field6',
                  'field7', 'field8', 'field9', 'field10', 'field11', 'field12', 'field13', 'field14', 'field15',
                  'field16', 'field17', 'field18', 'field19']

        widgets = {
            'report_date': forms.DateInput(attrs={'class': 'datepicker'}),
        }
