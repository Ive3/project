"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import never_cache
from django.conf.urls import handler404, handler500, handler403

urlpatterns = [
    path('thereisno_admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('captcha/', include('captcha.urls')),
    path('', include('mainapp.urls')),
    path('account/', include('registration.urls')),
    path('blog/', include('blog.urls')),
    path('shop/', include('shop.urls')),
    path('landing_page/', include('landingpage.urls')),
    path('gallery/', include('gallery.urls')),

]

handler404 = 'mainapp.views.my_error404'
handler403 = 'mainapp.views.my_error403'
handler500 = 'mainapp.views.my_error500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)