from django import forms
from .models import Case


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = '__all__'
        exclude = ['judge', 'added_date']

        widgets = {
            'status': forms.Select(attrs={
                'class': "form-control",
                'required': 'required',
            }),
            'case_type': forms.Select(attrs={
                'class': "form-control",
                'required': "required"
            }),
            'court': forms.Select(attrs={
                'class': "form-control",
                'required': "required"
            }),
            'case_num': forms.TextInput(attrs={
                'class': "form-control",
                'required': "required",
            }),
            'date': forms.DateInput(attrs={
                'class': "form-control",
                'required': "required",
                'type': 'date',
            }),
            'accused': forms.Textarea(attrs={
                'class': "form-control",
                'required': "required",
            }),
            'plaintiff': forms.Textarea(attrs={
                'class': "form-control",
                'required': "required",
            }),
            'aditional_text': forms.Textarea(attrs={
                'class': "form-control",
            })

        }
