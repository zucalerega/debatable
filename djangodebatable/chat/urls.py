from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.home, name = 'chathome'),
    path('<str:room>/', views.room, name = 'room'),
    path('checkview', views.checkview, name = 'checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name = 'getMessages'),
    path('<str:room>/rateview', views.rateview, name = 'rateview'),
    path('<str:room>/report', views.report, name = 'report'),
    path('<str:room>/leaveview', views.leaveview, name = 'leaveview')

]
