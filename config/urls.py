from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', include('registration.urls')),
    path('', include('home.urls')),

    # Module 05
    path('api/', include('registration.api_urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
LOGIN_REDIRECT_URL = '/registration/'
LOGOUT_REDIRECT_URL = '/accounts/login/'