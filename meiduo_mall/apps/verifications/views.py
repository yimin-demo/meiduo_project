from django.shortcuts import render

# Create your views here.
from django.views import View
from apps.users.models import User
from django.http import JsonResponse, HttpResponse
from django import http
from django_redis import get_redis_connection

import re
import json
from random import randint
import logging
logger = logging.getLogger('django')

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

    def get(self, request, mobile):
        """
        :param reqeust: 请求对象
        :param mobile: 手机号
        :return: JSON
        """

        # 1. extract request params
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        # 2. validate params
        if not all([image_code, uuid]):
            return JsonResponse({'code':400, 'errmsg':'参数不全'})

        # 3. verify image captcha
        redis_conn = get_redis_connection('code')
        redis_image_code = redis_conn.get(uuid)
        if redis_image_code is None:
            return JsonResponse({'code':400, 'errmsg':'图片验证码已过期'})
        if redis_image_code.decode().lower() != image_code.lower(): 
            return JsonResponse({'code':400, 'errmsg': '图片验证码错误'})
        
        # 4. generate sms code
        # sms_code = '%06d'%randint(100000,999999)
        sms_code = randint(1000, 9999)
        logger.info(sms_code)

        # 5. save sms code
        redis_conn.setex(mobile, 300, sms_code)
        
        # 6. send sms code
        from libs.yuntongxun.sms import send_message
        resp = send_message(mobile=str(mobile), datas=(str(sms_code), '5'))
        print(resp)

        # 7. return response
        return JsonResponse({'code':0, 'errmsg': '发送短信成功'})
