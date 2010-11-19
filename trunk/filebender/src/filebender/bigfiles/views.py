
import os
import os.path
import hashlib

from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.models import Site

from models import BigFile, Downloader, secret_generator, one_week_later
from forms import UploadForm


def mailit(to, from_, message, url):
    """
    compose and send an email
    """
    context = {'from': from_, 'url': url}
    body = render_to_string('email/download.html', context)
    send_mail('FileBender has a file for you!',
              body,
              'gijs@pythonic.nl',
    to, fail_silently=True)


def handle_uploaded_file(filename, secret, filedata):
    """
    Stores file into STORAGE. Returns MD5 of file
    """
    file_folder = os.path.join(settings.STORAGE_ROOT, secret)
    
    if not os.access(file_folder, os.F_OK):
        os.mkdir(file_folder)
        
    m = hashlib.md5()

    file_path = os.path.join(file_folder, filename)
    destination = open(file_path, 'wb+')
    for chunk in filedata.chunks():
        m.update(chunk)
        destination.write(chunk)
    destination.close()
    return m.hexdigest()


@login_required
def list(request):
    bigfiles = BigFile.objects.all()
    return render_to_response('bigfiles/list.html', {'bigfiles': bigfiles},
                              context_instance=RequestContext(request))

@login_required
def upload(request, js=False):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            data = request.FILES['file']
            name = form.cleaned_data['file'].name
            size = form.cleaned_data['file'].size
            expire_date = form.cleaned_data['expire_date'] or one_week_later()
            message = form.cleaned_data['message']
            receiver = form.cleaned_data['receiver']
            secret = secret_generator()
                
            md5 = handle_uploaded_file(name, secret, data)

            bigfile = BigFile(name=name, owner=request.user,
                        expire_date=expire_date, message=message, size=size,
                        md5=md5, secret=secret)
            bigfile.save()

            if receiver:
                downloader = Downloader(email=receiver, bigfile=bigfile)
                downloader.save()
                url = 'http://%s/bigfiles/download/%s/%s' % \
                    (Site.objects.get_current().domain, bigfile.id, secret)
                from_ = request.user.email
                mailit([receiver], from_, message, url)
                
            if js:
                return HttpResponse("done")
            return HttpResponseRedirect('/bigfiles/list/')
    else:
        form = UploadForm()


    if js:
        return HttpResponse("oops")   
    return render_to_response('bigfiles/upload.html',
                              {'form': form,},
                              context_instance=RequestContext(request))


def download(request, id, secret):
    bigfile = get_object_or_404(BigFile, pk=id)
    if secret != bigfile.secret:
        raise Http404
    return render_to_response('bigfiles/download.html', {'bigfile': bigfile},
                              context_instance=RequestContext(request))


@login_required
def delete(request, id):
    bigfile = get_object_or_404(BigFile, pk=id)

    file_folder = os.path.join(settings.STORAGE_ROOT, bigfile.secret)
    file_path = os.path.join(file_folder, bigfile.name)

    try:        
        os.remove(file_path)
    except OSError:
        # File is already gone
        pass
 
    if len(os.listdir(file_folder)) == 0:
        os.rmdir(file_folder)

    bigfile.delete()
    return HttpResponseRedirect('/bigfiles/list/')


@login_required
def edit(request, id):
    bigfile = get_object_or_404(BigFile, pk=id)

    file_folder = os.path.join(settings.STORAGE_ROOT, bigfile.secret)
    file_path = os.path.join(file_folder, bigfile.name)

    try:        
        os.remove(file_path)
    except OSError:
        # File is already gone
        pass
 
    if len(os.listdir(file_folder)) == 0:
        os.rmdir(file_folder)

    bigfile.delete()
    return HttpResponseRedirect('/bigfiles/list/')

