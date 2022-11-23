from django import forms


class AddWordsForm(forms.Form):
    words = forms.FileField(required=True, max_length=100)