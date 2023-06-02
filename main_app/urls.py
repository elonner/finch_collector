from django.urls import path
from . import views

urlpatterns = [
    path('', views.about, name='about'),
    path('finches/', views.FinchList.as_view(), name='index'),
    path('finches/<int:finch_id>/', views.finches_detail, name='detail'),
    path('finches/<int:finch_id>/add_feeding/', views.add_feeding, name='add_feeding'),
    path('finches/<int:finch_id>/add_photo/', views.add_photo, name='add_photo'),
    path('finches/<int:finch_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
    path('finches/<int:finch_id>/unassoc_toy/<int:toy_id>/', views.unassoc_toy, name='unassoc_toy'),
    path('finches/create/', views.FinchCreate.as_view(), name='create'),
    path('finches/<int:pk>/update/', views.FinchUpdate.as_view(), name='update'),
    path('finches/<int:pk>/delete/', views.FinchDelete.as_view(), name='delete'),
]