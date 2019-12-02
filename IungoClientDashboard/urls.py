from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from IungoClientDashboard.views import PortfolioView, Dashboard, AppointmentScheduler, Overview
from IungoClientDashboard import views

urlpatterns = [

    url(r'^portfolio/$', PortfolioView.as_view(), name=u'profile'),
    url(r'^$', Dashboard.as_view(), name=u'dashboard'),
    url(r'^appointment_scheduler/$', AppointmentScheduler.as_view(), name=u'appointment_scheduler'),
    url(r'^client_register$', views.client_register),
    url(r'^client_login$', views.client_login, name=u'client_login'),
    url(r'^auth$', views.auth_view, name=u'authenticate'),
    url(r'^customer_register$', views.customer_register),
    url(r'^overview/$', views.Overview, name=u'overview'),
]
