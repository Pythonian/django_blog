from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap

import blog.views
from blog.sitemaps import PostSitemap


sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path('', blog.views.home, name='home'),
    path('blog/', include('blog.urls', namespace='blog')),
    path('accounts/', include('allauth.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
