from django.conf import settings
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

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        *urlpatterns,
    ]

LOGIN_REDIRECT_URL = '/registration/'
LOGOUT_REDIRECT_URL = '/accounts/login/'