from django.conf.urls import url
from . import views

app_name ='core'

urlpatterns = [
    url(r'^test/(?P<test>[0-9])/problem/(?P<problem>[0-9])', views.showproblem ),
	url(r'^submit/test/(?P<test>[0-9])/problem/(?P<problem>[0-9])', views.submit , name='submit'),
]
