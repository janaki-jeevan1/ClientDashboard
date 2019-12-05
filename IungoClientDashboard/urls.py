from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from IungoClientDashboard.views import PortfolioView, Dashboard, AppointmentScheduler, Overview, welcome
from IungoClientDashboard import views

urlpatterns = [

    url(r'^portfolio/$', PortfolioView.as_view(), name=u'profile'),
    url(r'^portfolio/(?P<user_id>\d+)/$', PortfolioView.as_view(), name=u'profile'),
    url(r'^$', Dashboard.as_view(), name=u'dashboard'),
    url(r'^appointment_scheduler/$', AppointmentScheduler.as_view(), name=u'appointment_scheduler'),
    url(r'^client_register$', views.client_register, name=u'client_register'),
    url(r'^welcome', views.welcome, name=u'welcome'),
    url(r'^confirmation/(?P<confirmation_code>\w+)/(?P<username>\w+)$', views.confirmation),
    url(r'^client_login$', views.client_login, name=u'client_login'),
    url(r'^auth$', views.auth_view, name=u'authenticate'),
    url(r'^overview/$', views.Overview, name=u'overview'),
    url('load_sub_category$', views.load_sub_category, name='load_sub_category'),
]
