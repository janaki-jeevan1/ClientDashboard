from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from IungoClientDashboard.views import PortfolioView, Dashboard, AppointmentScheduler, Overview
from IungoClientDashboard import views

urlpatterns = [

    url(r'^portfolio/$', PortfolioView.as_view(), name=u'profile'),
    url(r'^$', Dashboard.as_view(), name=u'dashboard'),
    url(r'^appointment_scheduler/$', AppointmentScheduler.as_view(), name=u'appointment_scheduler'),
    url(r'^register$', views.register),
    url(r'^overview/$', views.Overview, name=u'overview'),
]
