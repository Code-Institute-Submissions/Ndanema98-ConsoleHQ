from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('summernote/', include('django_summernote.urls')),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('categories/<str:categories>/', views.products_by_category, name='products_by_category'),
    path('<int:product_id>/create_review/', views.create_review, name='create_review'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('newsletter/signup/', views.newsletter_signup, name='newsletter_signup'),

]
