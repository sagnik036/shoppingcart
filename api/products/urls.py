from django.urls import path
from . import views
urlpatterns = [
    path('listProducts/', views.ProductViews.as_view()),
    path('sellerProducts/', views.SellerProductView.as_view()),
]
