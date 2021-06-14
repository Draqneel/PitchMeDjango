from django.urls import path, include

from core.views import EventDetail, SearchListView, NotificationListView, NotificationDeleteView

app_name = 'core'

urlpatterns = [
    path('event/<int:pk>/', EventDetail.as_view(), name='event'),
    path('filter/<int:pk>/', SearchListView.as_view(), name='search_results'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('notification/delete/<int:pk>/', NotificationDeleteView.as_view(), name='delete_notify'),
]
