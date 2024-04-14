from django import forms


class DateForm(forms.Form):
    selected_date = forms.DateField(label='Выберите дату')
