from django.urls import path

from . import views

urlpatterns = [
    path("wiki/<str:title>",views.wikiEntry,name="wikiEntry"),
    path("random-page",views.randomPage,name="random-page"),
    path("edit-entry/<str:title>",views.editEntry,name="edit-entry"),
    path("search-results", views.search, name="search"),
    path("new-page",views.newPage, name="new-page"),
    path("", views.index, name="index"),



    
]
