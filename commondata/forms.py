from django import forms
from django.contrib.admin.widgets import AdminDateWidget


class DateForm(forms.Form):
    selected_date = forms.DateField(label='Выберите дату',
                                    input_formats=['%d.%m.%Y'],
                                    widget=AdminDateWidget()
                                    )


class DateSelectionForm(forms.Form):
    report_date = forms.DateField(label='Выберите дату сводного отчёта (в формате дд.мм.гггг)',
                                  input_formats=['%d.%m.%Y'],
                                  widget=AdminDateWidget()
                                  )


class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=AdminDateWidget(), label="Начальная дата")
    end_date = forms.DateField(widget=AdminDateWidget(), label="Конечная дата")

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError("Конечная дата не может быть раньше начальной даты.")
        else:
            raise forms.ValidationError("Все поля должны быть заполнены.")

        return cleaned_data
