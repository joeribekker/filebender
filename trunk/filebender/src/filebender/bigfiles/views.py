from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.conf import settings
from django.core.mail import send_mail

import os.path

from models import BigFile, Downloader
from forms import UploadForm


# TODO: make better
# http://docs.djangoproject.com/en/1.2/topics/http/file-uploads/

# TODO: maybe use custom upload handler
# http://docs.djangoproject.com/en/1.2/topics/http/file-uploads/#upload-handlers

def handle_uploaded_file(filename, filedata):
    file_location = os.path.join(settings.STORAGE_ROOT, filename)
    destination = open(file_location, 'wb+')
    for chunk in filedata.chunks():
        destination.write(chunk)
    destination.close()


@login_required
def list(request):
    bigfiles = BigFile.objects.all()
    return render_to_response('bigfiles/list.html', {'bigfiles': bigfiles},
                              context_instance=RequestContext(request))

def mailit(to, message, url):
    body = "%s \n\n Download URL: %s" % (message, url)
    send_mail('A file for you',
              body,
              'gijs@pythonic.nl',
    to, fail_silently=False)


@login_required
def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            filedata = request.FILES['file']
            filename = form.cleaned_data['file'].name
            expire_date = form.cleaned_data['expire_date']
            message = form.cleaned_data['message']
            receiver = form.cleaned_data['receiver']
            handle_uploaded_file(filename, filedata)  
            bigfile = BigFile(data=filename, owner=request.user,
                        expire_date=expire_date, message=message)
            bigfile.save()
            downloader = Downloader(email=receiver, bigfile=bigfile)
            downloader.save()
            mailit([receiver], message, file.data.url)
            return HttpResponseRedirect('/bigfiles/list/')
    else:
        form = UploadForm()

    return render_to_response('bigfiles/upload.html',
                              {'form': form,},
                              context_instance=RequestContext(request))

def download(request, id, secret):
    file = get_object_or_404(BigFile, pk=id)
    if secret != file.secret:
        raise Http404
    return render_to_response('bigfiles/download.html', {'file': file},
                              context_instance=RequestContext(request))


def delete(request, id):
    file = get_object_or_404(BigFile, pk=id)
    file.delete()
    return HttpResponseRedirect('/bigfiles/list/')

