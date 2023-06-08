from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<item_id>/', views.add_to_bag, name='add_to_bag'),
    path('adjust/<item_id>/', views.adjust_bag, name='adjust_bag'),
    path(
        'remove/<item_id>/', views.delete_item_bag, name='delete_item_bag'),
    path(
        'subscribe_to_newsletter/', views.subscribe_to_newsletter, name='subscribe_to_newsletter'),

]
