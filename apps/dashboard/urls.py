from django.conf.urls import url

from . import views

app_name = 'dashboard'
urlpatterns = [
    url(r'^$', views.dashboard, name="my_dashboard"),
    url(r'^admin$', views.admin, name="my_admin_dashboard"),
]

