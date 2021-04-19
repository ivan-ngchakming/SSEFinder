from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('cases', views.cases, name='cases'),
    path('events', views.events, name='events'),
    path('cases/<int:id>', views.case, name='case'),
    path('events/<int:id>', views.event, name='event'),
]
