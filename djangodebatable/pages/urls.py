from django.urls import path
from . import views
from .views import ResourceListView, ResourceDetailView, resource_list_view

app_name = 'resources'
urlpatterns = [
    path('', resource_list_view, name='resource-list'),
    path('<int:pk>/', ResourceDetailView.as_view(), name="resource")
]
