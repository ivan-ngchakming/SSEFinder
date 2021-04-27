from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('ajax', views.query_case_detail, name='query_case_detail'),
    path('ajax/SSE_Loc', views.events, name='events'),
]
