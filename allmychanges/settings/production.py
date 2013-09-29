from .default import *

REST_FRAMEWORK.update({
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
})


RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 1,
        'PASSWORD': '',
   },
}

DATABASES['default'].update({
    'NAME': 'allmychanges',
})

GRAPHITE_PREFIX = 'allmychanges'

ALLOWED_HOSTS = ['allmychanges.com']

SHOW_METRIKA = True
