from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# from two_factor.urls import urlpatterns as tf_urls

# This is for 'Token based authentication in rest-framework:
# from rest_framework.authtoken import views as token_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),     # Enable 'ckeditor' editor
    path('__debug__/', include('debug_toolbar.urls')),    # Enable 'django-debug-toolbar'
    path('silk/', include('silk.urls', namespace='silk')),    # Enable 'django-silk'
    path('watchman/', include('watchman.urls')),    # Enable 'django-watchman'
    path('api-auth/', include('rest_framework.urls')),    # ...defined as 'accounts' subdirectory in 'hosts.py' module
    # path('token-auth/', token_view.obtain_auth_token),    # But in this example 'accounts.tests' module only works with

    path('login/', include('login.urls')),
    path('', include('vitrin.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
