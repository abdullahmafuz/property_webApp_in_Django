from celery import shared_task
from time import sleep
from django.contrib import messages

@shared_task
def sleeps(duration):
    sleep(duration)
    print('done')
    return 'form submitted'
    

