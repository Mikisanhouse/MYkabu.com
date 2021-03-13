from django import forms


class CodeForm(forms.Form):
    code1 = forms.CharField(max_length=10)
    code2 = forms.CharField(max_length=10)
