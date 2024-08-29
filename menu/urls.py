from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('menu/<slug:menu_slug>/', views.MenuDetailView.as_view(), name='menu_detail'),
    path('menu/', views.MenuView.as_view(), name='menu_list'),
    path('menu/<path:item_path>/', views.ItemDetailView.as_view(), name='item_detail')
]
