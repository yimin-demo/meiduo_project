from celery import Celery

# 为celery使用django配置文件进行设置
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings")

app = Celery('meiduo')
app.config_from_object('meiduo.config')