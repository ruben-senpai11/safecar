from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Myroad.settings')
app = Celery('Myroad')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
    
    
    
app.conf.beat_schedule = {
    #Scheduler Name
    'print-message-ten-seconds': {
        # Task Name (Name Specified in Decorator)
        'task': 'print_msg_main',  
        # Schedule      
        'schedule': 10.0,
        # Function Arguments 
        'args': ("Hello",) 
    },
    #Scheduler Name
    'print-time-twenty-seconds': {
        # Task Name (Name Specified in Decorator)
        'task': 'print_time',  
        # Schedule      
        'schedule': 20.0, 
    },
    #Scheduler Name
    'calculate-forty-seconds': {
        # Task Name (Name Specified in Decorator)
        'task': 'get_calculation',  
        # Schedule      
        'schedule': 40.0,
        # Function Arguments 
        'args': (10,20) 
    },
}  



#from https://realpython.com