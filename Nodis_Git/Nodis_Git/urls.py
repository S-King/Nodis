"""
Definition of urls for Nodis.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()


## Add redirection for already logged in users when I have time ##
# url(r'^login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),


urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^template$', app.views.template, name='template'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    ######### Account Activation #########
    url(r'^account_activation_sent$', app.views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        app.views.activate, name='activate'),
    url(r'^signup/$', app.views.signup, name='signup'),
    ######################################

    ######### Logged in Routes ###########
    url(r'^dashboard$', app.views.dashboard, name='Dashboard'),
    url(r'^account$', app.views.account, name='Account'),
    ######################################




    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
