from django.conf.urls import url
from . import views

app_name ='run'

urlpatterns = [
    url(r'^run/', views.run ),
]
