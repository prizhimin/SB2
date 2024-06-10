from django import forms
from .models import SemiAnnual2024Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = SemiAnnual2024Report
        fields = [
            'company',
            'field_1', 'field_2', 'field_3', 'field_4', 'field_5', 'field_6', 'field_7', 'field_8', 'field_9',
            'field_10', 'field_11', 'field_12', 'field_13', 'field_14', 'field_15', 'field_16', 'field_17', 'field_18',
            'field_19', 'field_20', 'field_21', 'field_22', 'field_23', 'field_24', 'field_25', 'field_26', 'field_27',
            'field_28', 'field_29', 'field_30', 'field_31', 'field_32', 'field_33', 'field_34', 'field_35', 'field_36',
            'field_37', 'field_38', 'field_39', 'field_40', 'field_41', 'field_42', 'field_43', 'field_44', 'field_45',
            'field_46', 'field_47', 'field_48', 'field_49', 'field_50', 'field_51'
        ]


