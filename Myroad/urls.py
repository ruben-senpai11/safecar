from django.conf import settings

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from safecar import views

urlpatterns = [
    path('safecar/', include('safecar.urls')),
    path('admin/', admin.site.urls),
    path('api/tag/',views.tag_api,name="tag_api"),
    path('api/tag/read/',views.read,name="tag_read"),
    path('api/tag/check/',views.send_mail_to_user,name="tag_read"),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
