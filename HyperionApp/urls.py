from datetime import datetime
from django.conf.urls import url, include
from django.contrib import admin
import django.contrib.auth.views
import app.forms
import app.views
import app.urls

admin.autodiscover()

urlpatterns = [
    url(r'^$', app.views.home, name='home'),
    url(r'^app/', include('app.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/', app.views.UserFormView.as_view(), name='register'),
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
]
