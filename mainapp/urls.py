from django.urls import path
from .views import BaseView, ItemDetailView, AddSaleView

app_name = 'mainapp'
urlpatterns = [
    path('', BaseView.as_view(), name = 'index'),
    path('items/<str:slug>/', ItemDetailView.as_view(), name = 'detail'),
    path('add_sale/<str:slug>/', AddSaleView.as_view(), name = 'add_sale'),
]
