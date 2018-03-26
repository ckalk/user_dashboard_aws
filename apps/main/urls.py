from django.conf.urls import url

from . import views

app_name = 'main'
urlpatterns = [
	url(r'^$', views.index, name="my_index"),
    url(r'^signin$', views.signin, name="my_signin"),
    url(r'^login$', views.login, name="my_login"),
    url(r'^register$', views.register, name="my_register"),
    url(r'^create_user$', views.create_user, name="my_create_user"),
    url(r'^logoff$', views.logoff, name="my_logoff"),
]

