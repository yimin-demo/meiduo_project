from celery_tasks.main import app
from libs.yuntongxun.sms import send_message
import logging
logger = logging.getLogger('django')