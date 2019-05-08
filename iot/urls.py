from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('reports/', include('reports.urls')),
    path('login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': 'login'}, name='logout'),
    path('tenants/', include('tenants.urls')),
    path('api/', include('api.urls')),
    path('notifications/', include('notifications.urls')),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'IoT Dashboard'
admin.site.site_title = 'IoT Dashboard'
admin.site.index_title = 'Admin'
