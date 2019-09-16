from django.shortcuts import render
from django.views import View
from django.http import HttpResponse,HttpResponseRedirect
from .models import UserDetail, UserModel
from .form import RegisterForm
import hashlib
import random
import requests
import os
import time
import json
import base64
# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header



# 展示主页面
class Home(View):
    def get(self, request):
        # 如果登陆过，获取用户名。未登陆过的话，返回未登录
        username = request.session.get('username', '未登录')
        if username == '未登录':
            return HttpResponseRedirect('/login')
        tem = UserDetail.objects.filter(username=username).values()[0]['tem'][2:4]
        hum = UserDetail.objects.filter(username=username).values()[0]['hum'][2:4]
        bright = UserDetail.objects.filter(username=username).values()[0]['bright'][2:5]
        status = UserDetail.objects.filter(username=username).values()[0]['door_status']
        key = UserDetail.objects.filter(username=username).values()[0]['device_key']
        if status == 'open':
            return render(request, 'lock/home-open.html', locals())
        return render(request, 'lock/home-close.html', locals())



# 页面开关的API
class PageButton(View):
    def get(self, request):
        # 如果登陆过，获取用户名。未登陆过的话，返回未登录
        username = request.session.get('username', '未登录')
        if username == '未登录':
            return HttpResponseRedirect('/login')
        status = UserDetail.objects.filter(username=username).values()[0]['door_status']
        if status == 'close':
            # 发送开门的请求
            key = UserDetail.objects.filter(username=username).values()[0]['device_key']
            url = 'http://2562449r2q.zicp.vip/open/?key={}'.format(key)
            # print('返回值：',requests.get(url).text)
            UserDetail.objects.filter(username=username).update(door_status='open')
            return HttpResponseRedirect('/home')
        if status == 'open':
            UserDetail.objects.filter(username=username).update(door_status='close')
            return HttpResponseRedirect('/home')



# Create your views here.
class Register(View):
    def get(self, request):
        return render(request, 'lock/register.html')

    def post(self, request):
        # 获取post传入的值，传给form验证
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 获取每个值
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            password_repeat = form.cleaned_data.get('password_repeat')
            if password == password_repeat:
                password_md5 = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
                UserModel.objects.create(username=username, password=password_md5)
                random_num = str(random.random())
                device_key = hashlib.md5(random_num.encode(encoding='UTF-8')).hexdigest()
                UserDetail.objects.create(username=username, device_key=device_key,
                                         tem='30',hum='60',bright='10',door_status='open')
                return render(request, 'lock/ok.html', locals())
                # return HttpResponse('注册成功，请记住你的设备密钥：'+device_key)
            else:
                return HttpResponseRedirect('/register')
        else:
            return HttpResponseRedirect('/register')



# 登陆
class Login(View):
    def get(self, request):
        return render(request, 'lock/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_md5 = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
        User = UserModel.objects.filter(username=username).values()
        if User and User[0]['password']==password_md5:
            request.session['username'] = username
            return HttpResponseRedirect('/home')
        return HttpResponse('账户名密码错误！')



# 推出登陆
class Logout(View):
    def get(self, request):
        request.session.flush()  # 键和值一起清空
        return HttpResponseRedirect('/home')



# 传感器数据上传API
class SensorData(View):
    def get(self, request):
        key = request.GET.get('key')
        tem = request.GET.get('tem')
        hum = request.GET.get('hum')
        bright = request.GET.get('bright')
        UserDetail.objects.filter(device_key=key).update(tem=tem, hum=hum, bright=bright)
        return HttpResponse('1')



# 人脸识别修改门锁的状态值
class UpdateStatus(View):
    def get(self, request):
        key = request.GET.get('key')
        status = request.GET.get('door_status')
        # print('status：',status)
        UserDetail.objects.filter(device_key=key).update(door_status=status)
        return HttpResponse('1')



# 开门的API
class OpenDoor(View):
    def get(self, request):
        username = request.session.get('username', '未登录')
        key = UserDetail.objects.filter(username=username).values()[0]['device_key']
        # print(key)
        url = 'http://2562449r2q.zicp.vip/open/?key={}'.format(key)
        requests.get(url)
        return HttpResponse('1')



# 上传视频的接口
class VideoData(View):
    def get(self, request):
        video_name = request.GET.get('video_name')
        video_name_url = video_name.split('.')[0]
        url = 'http://2562449r2q.zicp.vip/response_video?video_name={}'.format(video_name)
        video_data = requests.get(url).content
        path1 = r'/var/www/face/static/video/{}.mp4'.format(video_name_url)
        with open(path1, 'wb') as f:
            f.write(video_data)
        # self.send_email(video_name)                                      # 发送邮件
        return HttpResponse('1')







# # 添加人脸
# class AddFace(View):
#     def get(self, request):
#         get_face_file_url = 'http://2562449r2q.zicp.vip/add_face'
#         file_name_str = requests.get(get_face_file_url).text
#         # print(file_name_str)
#         file_name_list = [file_name_str[0]+'.jpg',file_name_str[5]+'.jpg',file_name_str[10]+'.jpg']
#         dir_name = str(int(time.time()))
#         saveDir = '/var/www/face/static/images/'+dir_name
#         os.makedirs(saveDir)
#         for name in file_name_list:
#             url = 'http://2562449r2q.zicp.vip/response_img?file_name='+name
#             img_data = requests.get(url).content
#             with open(saveDir+'/'+name, 'wb') as f:
#                 f.write(img_data)
#         return  HttpResponseRedirect('/show_face?path='+saveDir+'&dir_name='+dir_name)



# # 展示人脸的照片
# class ShowFaceImg(View):
#     def get(self, request):
#         path = request.GET.get('path')
#         dir_name = request.GET.get('dir_name')
#         img_list = os.listdir(path)
#         base_url = 'http://kuailezhai.cn/static/images/'+dir_name
#         img_url = [base_url+'/'+u for u in img_list]
#         return render(request, 'lock/show_face.html', locals())



# # 将人脸添加到人脸库中
# class AddFaceAPI(View):
#     def get(self, request):
#         username = request.session.get('username', '未登录')
#         url = 'https://aip.baidubce.com/rest/2.0/face/v3/faceverify?access_token=24.4ca2f418c892a992ad313b20cb36194d.2592000.1564465193.282335-16676879'
#
#         img_url = request.GET.get('img_url')
#         print('img_url',img_url)
#         img_url = 'http://kuailezhai.cn/static/images/'+ img_url
#         img_data = requests.get(img_url).content
#         image = base64.b64encode(img_data)
#
#         headers = {
#             'Content-Type': 'application/json',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
#         }
#         data = [{
#             'image':image,
#             'image_type':'BASE64',
#             'group_id':'jiang',
#             'user_id':username,
#         }]
#         # data = json.dumps(data)
#         response = requests.post(url, headers=headers, data=data).text
#         print('response',response)
#         return HttpResponse('1')




# APP登陆接口
class AppLogin(View):
    def get(self, request):
        username = request.GET.get('username')
        password = request.GET.get('password')
        # print('username',username)
        # print('password',password)
        password_md5 = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
        User = UserModel.objects.filter(username=username).values()
        if User and User[0]['password']==password_md5:
            return HttpResponse('true')
        return HttpResponse('false')



# 给app,返回数据
class AppSensorData(View):
    def get(self, request):
        username = request.GET.get('username')
        tem = UserDetail.objects.filter(username=username).values()[0]['tem'][2:4]
        hum = UserDetail.objects.filter(username=username).values()[0]['hum'][2:4]
        bright = UserDetail.objects.filter(username=username).values()[0]['bright'][2:5]
        status = UserDetail.objects.filter(username=username).values()[0]['door_status']
        data = {
            'tem': tem,
            'hum': hum,
            'bright': bright,
            'door_status': status
        }
        data = json.dumps(data)
        return HttpResponse(data)



# APP 注册
class AppRegister(View):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_md5 = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
        UserModel.objects.create(username=username, password=password_md5)
        random_num = str(random.random())
        device_key = hashlib.md5(random_num.encode(encoding='UTF-8')).hexdigest()
        UserDetail.objects.create(username=username, device_key=device_key,
                                 tem='30',hum='60',bright='10',door_status='open')
        return HttpResponse('true')






