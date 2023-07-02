from django.urls import path

from . import views


app_name = 'vitrin'

urlpatterns = [
    path('find-product/', views.find_product, name='find-product'),
    path('', views.index, name='index'),
]
