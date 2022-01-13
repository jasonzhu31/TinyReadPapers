from django.http import JsonResponse
from django.http import HttpResponse
from login_module.models import usr_info

def ResponseOk(message=''):
    return JsonResponse({'status':'ok', 'message':message, 'errorcode':0})

def ResponseError(message='', errorcode=0):
    return JsonResponse({'status':'error', 'message':message, 'errorcode':errorcode})

def sayHello(request):
    usr_info.objects.all().delete()
    return JsonResponse({'message':'Hello'})

def login(request):
    print(request.GET)
    username = request.GET['username']
    password = request.GET['password']
    query_set_1 = usr_info.objects.filter(username=username)
    query_set_2 = usr_info.objects.filter(username=username, password=password)
    if len(query_set_1) == 0:
        msg = 'The user does not exist!'
        return ResponseError(msg, 1)
    else:
        if len(query_set_2) > 0:
            msg = query_set_2.values('last_path')[0]
            print(msg)
            return ResponseOk(msg)
        else:
            msg = 'The username and password are not matched!'
            return ResponseError(msg, 2)
    return ResponseOk(msg)

def register(request):
    print(request.GET)
    data = request.GET
    user_info_dict = {
        'username':data['username'],
        'password':data['password'],
        'email':data['email']
    }
    if len(usr_info.objects.filter(username=data['username'])) > 0:
        return ResponseError('The name has been used!', 1)
    if len(usr_info.objects.filter(email=data['email'])) > 0:
        return ResponseError('The email address has been used!', 2)
    usr_info.objects.create(**user_info_dict)
    return ResponseOk()