from cloudfn.django_handler import handle_http_event
from mysite.wsgi import application


handle_http_event(application)
