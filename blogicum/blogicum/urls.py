from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import CreateView

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/', CreateView.as_view(), name='registration'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug/', include(debug_toolbar.urls)),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
