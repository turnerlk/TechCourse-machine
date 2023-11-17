from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from accounts.views import login_view, logout_view, change_the_password_view, index_view, monitor_logs
from curso.views import curso_view, CouseDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('course/', curso_view, name='course'),
    path('change_password', change_the_password_view, name='change_password'),
    path('curso/<int:pk>/', CouseDetailView.as_view(), name='curso_detail'),
    path('monitor_logs/', monitor_logs, name='monitor_logs'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
