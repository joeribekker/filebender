from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import File
from forms import UploadForm


# TODO: make better
# http://docs.djangoproject.com/en/1.2/topics/http/file-uploads/

# TODO: maybe use custom upload handler
# http://docs.djangoproject.com/en/1.2/topics/http/file-uploads/#upload-handlers

def handle_uploaded_file(f):
    destination = open('/tmp/upload.txt', 'wb+')
    for chunk in f.chunks():
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
        if form.is_valid() and len(request.FILES) == 1:
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/files/list/')
    else:
        form = UploadForm()

    return render_to_response('files/upload.html',
                              {'form': form,},
                              context_instance=RequestContext(request))

def download(request, file_id):
    pass
