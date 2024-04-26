from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('wiki/<title>', views.get_entry, name="get_entry"),
    path('search', views.search, name="search")
]
