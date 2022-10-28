from django.urls import path
from . import views
urlpatterns = [
    path('', views.ProductViews.as_view()),
    path('sellerProducts/', views.SellerProductView.as_view()),
]
