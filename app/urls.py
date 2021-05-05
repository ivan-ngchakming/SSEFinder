from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/case_detail', views.case_detail, name='Case detail'),
    path('ajax/SSE_Loc', views.events, name='Events'),
    path('ajax/event_detail', views.event_detail, name='Event detail'),
    path('ajax/showrecordform', views.create_post, name='ShowRecord'),
    path('ajax/event_detail', views.event_detail, name='Event detail'),
    path('ajax/add_newcase', views.addcase, name='Add case'),
    path('ajax/success-page', views.success, name='success'),
]
