from django import forms


class GetChangeLogForm(forms.Form):
    repository = forms.CharField()
