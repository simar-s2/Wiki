from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('wiki/<title>/', views.get_entry, name="get_entry"),
    path('search', views.search, name="search"),
    path('create_page', views.create_page, name="create_page"),
    path('random', views.random_selector, name="random_selector"),
    path('edit/<title>', views.edit_page, name="edit_page"),
]
