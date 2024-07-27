from django import forms
from .models import Investigation, AttachedFile, InvestigationUserDepartment, Department


class InvestigationForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_departments = InvestigationUserDepartment.objects.filter(user=user)
        department_ids = user_departments.values_list('department__id', flat=True)
        self.fields['department'].queryset = Department.objects.filter(id__in=department_ids).order_by('name')
        self.fields['damage_amount'].required = False
        self.fields['recovered_amount'].required = False
        self.fields['outcome_summary'].required = False
        self.fields['num_employees_discipline'].required = False
        self.fields['order_date'].input_formats = ['%d.%m.%Y']
        self.fields['end_date'].input_formats = ['%d.%m.%Y']
        self.fields['extended_end_date'].input_formats = ['%d.%m.%Y']

    class Meta:
        model = Investigation
        fields = ['title', 'department', 'order_date', 'order_num', 'brief_summary',
                  'initiator', 'end_date', 'extended_end_date', 'status', 'damage_amount',
                  'recovered_amount', 'outcome_summary', 'num_employees_discipline']
        widgets = {
            'order_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'end_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'extended_end_date': forms.DateInput(attrs={'class': 'datepicker'}),
        }


class AttachedFileForm(forms.Form):
    file = forms.FileField()

    def save(self, investigation):
        uploaded_file = self.cleaned_data['file']
        attached_file = AttachedFile(
            investigation=investigation,
            file=uploaded_file
        )
        attached_file.save()


class DateForm(forms.Form):
    selected_date = forms.DateField(label='Выберите дату',
                                    input_formats=['%d.%m.%Y'],
                                    widget=forms.DateInput(attrs={'class': 'datepicker'}),
                                    )
