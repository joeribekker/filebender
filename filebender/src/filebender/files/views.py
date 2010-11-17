from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.conf import settings

import os.path

from models import File
from forms import UploadForm


# TODO: make better
# http://docs.djangoproject.com/en/1.2/topics/http/file-uploads/

# TODO: maybe use custom upload handler
# http://docs.djangoproject.com/en/1.2/topics/http/file-uploads/#upload-handlers

def handle_uploaded_file(filename, filedata):
    file_location = os.path.join(settings.MEDIA_ROOT, filename)
    destination = open(file_location, 'wb+')
    for chunk in filedata.chunks():
        destination.write(chunk)
    destination.close()


@login_required
def list(request):
    files = File.objects.all()
    return render_to_response('files/list.html', {'files': files}, context_instance=RequestContext(request))


@login_required
def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            filedata = request.FILES['file']
            filename = form.cleaned_data['file'].name
            expire_date = form.cleaned_data['expire_date']
            message = form.cleaned_data['message']
            handle_uploaded_file(filename, filedata)  
            file = File(data=filename, owner=request.user,
                        expire_date=expire_date, message=message)
            file.save()
            return HttpResponseRedirect('/files/list/')
    else:
        form = UploadForm()

    return render_to_response('files/upload.html',
                              {'form': form,},
                              context_instance=RequestContext(request))

def download(request, id):
    file = get_object_or_404(File, pk=id)
    return render_to_response('files/download.html', {'file': file})


def delete(request, id):
    file = get_object_or_404(File, pk=id)
    file.delete()
    return HttpResponseRedirect('/files/list/')

