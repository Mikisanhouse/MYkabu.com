import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '!)0a&%vul0+*5qx$ci5b34f5*kx45hkopr%w43(___&x-js)o_'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


DEBUG = True
