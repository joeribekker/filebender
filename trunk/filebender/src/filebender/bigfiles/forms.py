
from django import forms
import datetime

class UploadForm(forms.Form):
    file = forms.FileField('File')
    message = forms.CharField(widget=forms.Textarea(),label='Message',
                              required=False)
    receiver = forms.EmailField(label='Receiver')
    
    default_expire = datetime.datetime.now() + datetime.timedelta(weeks=1)
    expire_date = forms.DateTimeField(label='Expire date', initial=default_expire)


