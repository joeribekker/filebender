
from django import forms

class UploadForm(forms.Form):
    file = forms.FileField()
    message = forms.CharField(widget=forms.Textarea())
    receiver = forms.EmailField()


