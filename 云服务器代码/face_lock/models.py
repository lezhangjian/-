from django.db import models

# Create your models here.
class UserModel(models.Model):
    username = models.CharField(max_length=150, primary_key=True)
    password = models.CharField(max_length=150)




# 用户的详情信息
class UserDetail(models.Model):
    username = models.CharField(max_length=150)
    device_key = models.CharField(max_length=150)
    tem = models.CharField(max_length=150)
    hum = models.CharField(max_length=150)
    bright = models.CharField(max_length=150)
    door_status = models.CharField(max_length=150)