from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from service.settings import NOTE_FILE_SYSTEM_ROOT, PAPER_FILE_SYSTEM_ROOT 
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import FileResponse
from login_module.models import usr_info
from google_trans_new import google_translator
import sys

# https://blog.csdn.net/h18208975507/article/details/110875361

def ResponseOk(message=''):
    return JsonResponse({'status':'ok', 'message':message})

def ResponseJson(data={}):
    return JsonResponse({'status':'ok', 'data':data})

def ResponseFile(file):
    return FileResponse(file)

# Create your views here.

def process_path(path):
    if (path == ''):
        return '.'
    else:
        return path[1:]

def test(request):
    note_fs = FileSystemStorage(location=NOTE_FILE_SYSTEM_ROOT + '/User1')
    note_fs.delete('1.txt')
    path = note_fs.save('1.txt', ContentFile('new content'))
    print(note_fs.open(path).read())
    print(path)
    print(note_fs.listdir('.'))
    print(note_fs.exists('1.txt'))
    return ResponseOk()

def upload_pdf(request):
    username = request.COOKIES['username']
    pdf = request.FILES.get('pdf')
    path = request.POST.get('path')
    name = request.POST.get('name')
    print(request.POST)
    
    fs = FileSystemStorage(location=PAPER_FILE_SYSTEM_ROOT + '/' + username + path)
    if name != '.':
        fs.save(name, pdf)
    else:
        fs.save(pdf.name, pdf)
    
    return ResponseOk()

def checkdir(request):
    username = request.COOKIES['username']
    path = request.POST.get('path')
    path = process_path(path)
    print(path)
    fs = FileSystemStorage(location=PAPER_FILE_SYSTEM_ROOT + '/' + username)
    if fs.exists(path):
        return ResponseOk('yes')
    else:
        return ResponseOk('no')

def listdir(request):
    username = request.COOKIES['username']
    current_path = request.POST['path']
    current_path = process_path(current_path)
    fs = FileSystemStorage(location=PAPER_FILE_SYSTEM_ROOT + '/' + username)
    print('current_path = ',current_path)
    return ResponseJson(fs.listdir(current_path))

def open(request):
    username = request.COOKIES['username']
    path = request.POST['path']
    usr_info.objects.filter(username=username).update(last_path=path)
    return ResponseOk()

def last_path(request):
    username = request.COOKIES['username']
    last_path = usr_info.objects.filter(username=username).values('last_path')[0]
    return ResponseJson(last_path)

def remove(request):
    username = request.COOKIES['username']
    path = request.POST['path']
    path = process_path(path)
    fs = FileSystemStorage(location=PAPER_FILE_SYSTEM_ROOT + '/' + username)
    fs.delete(path)
    return ResponseOk()

def translate(request):
    #sys.setdefaultencoding( "utf-8" )
    text = request.POST['text']
    dest = request.POST['dest']
    print(text)
    translator = google_translator()
    result = translator.translate(text, dest)
    print(result)
    return ResponseJson(result)