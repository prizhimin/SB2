from django import forms


class DateForm(forms.Form):
    selected_date = forms.DateField(label='Выберите дату', input_formats=['%d.%m.%Y'])


class DateSelectionForm(forms.Form):
    report_date = forms.DateField(label='Выберите дату сводного отчёта (в формате дд.мм.гггг)',
                                  input_formats=['%d.%m.%Y'])
