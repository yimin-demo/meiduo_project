from celery_tasks.main import app
from libs.yuntongxun.sms import send_message
import logging
logger = logging.getLogger('django')

@app.task
def celery_send_sms_code(mobile, datas):

    try:
        send_message(mobile=mobile, datas=datas)
    except Exception as e:
        logger.error(e)