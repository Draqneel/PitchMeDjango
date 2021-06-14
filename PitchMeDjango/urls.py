from django.contrib import admin
from django.urls import path, include

from core.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('accounts/', include('allauth.urls')),
]
