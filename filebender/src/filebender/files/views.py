from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings

import os.path

from models import File
from forms import UploadForm


# TODO: make better
# http://docs.djangoproject.com/en/1.2/topics/http/file-uploads/

# TODO: maybe use custom upload handler
# http://docs.djangoproject.com/en/1.2/topics/http/file-uploads/#upload-handlers

@login_required
def list(request):
    files = File.objects.all()
    return render_to_response('files/list.html', {'files': files}, context_instance=RequestContext(request))


@login_required
def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            filename = form.cleaned_data['file'].name
            expire_date = form.cleaned_data['expire_date']
            message = form.cleaned_data['message']
            location = settings.MEDIA_ROOT
            file_location = os.path.join(location, filename)
            destination = open(file_location, 'wb+')        
            for chunk in f.chunks():
                destination.write(chunk)
            file = File(data=file_location, owner=request.user,
                        expire_date=expire_date, message=message)
            file.save()
            return HttpResponseRedirect('/files/list/')
    else:
        form = UploadForm()

    return render_to_response('files/upload.html',
                              {'form': form,},
                              context_instance=RequestContext(request))

def download(request, file_id):
    pass
