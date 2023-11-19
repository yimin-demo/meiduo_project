from django.shortcuts import render

# Create your views here.
from django.views import View
from apps.users.models import User
from django.http import JsonResponse, HttpResponse
from django import http
from django_redis import get_redis_connection

import re
import json

# Create your views here.
class ImageCodeView(View):
    """图形验证码"""

    def get(self, request, uuid):
        """
        :param request: 请求对象
        :param uuid: 唯一标识图形验证码所属于的用户
        :return: image/jpeg
        """

        from libs.captcha.captcha import captcha
        text, image = captcha.generate_captcha()

        redis_conn = get_redis_connection('code')
        redis_conn.setex(uuid, 300, text)

        return HttpResponse(image, content_type='image/jpeg')
    

class SMSCodeView(View):

    def get(self, reqeust, mobile):
        """
        :param reqeust: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        
        from libs.yuntongxun.sms import send_message