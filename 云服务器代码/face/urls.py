"""face URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from face_lock.views import Register, Logout, Login, SensorData, Home, OpenDoor, VideoData, UpdateStatus, AppLogin, PageButton
from face_lock.views import  AppSensorData, AppRegister


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^register/', Register.as_view()),
    url(r'^login/$', Login.as_view()),
    url(r'^logout/', Logout.as_view()),
    url(r'^sensor_data', SensorData.as_view()),
    url(r'^home/', Home.as_view()),
    url(r'^open_door/', OpenDoor.as_view()),
    url(r'^video_data/', VideoData.as_view()),
    url(r'^update_data/', UpdateStatus.as_view()),
    url(r'^app_login/', AppLogin.as_view()),
    url(r'^page_button/', PageButton.as_view()),
    # url(r'^add_face/', AddFace.as_view()),
    # url(r'^show_face/', ShowFaceImg.as_view()),
    url(r'^app_sensor_data/', AppSensorData.as_view()),
    url(r'^app_register/', AppRegister.as_view()),
    # url(r'^add_face_api/', AddFaceAPI.as_view()),
]
