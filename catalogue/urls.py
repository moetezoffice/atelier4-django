from django.urls import path

from . import views

app_name = "catalogue"

urlpatterns = [
    path("livres/", views.livre_list, name="livre_list"),
    path("livres/<int:pk>/", views.livre_detail, name="livre_detail"),
    path("livres/ajouter/", views.livre_create, name="livre_create"),
    path("livres/<int:id>/edit/", views.livre_update, name="livre_update"),
    path("livres/<int:id>/delete/", views.livre_delete, name="livre_delete"),
    path("auteurs/", views.auteur_list, name="auteur_list"),
    path("auteurs/<int:pk>/", views.auteur_detail, name="auteur_detail"),
    path("auteurs/ajouter/", views.auteur_create, name="auteur_create"),
    path("auteurs/<int:id>/edit/", views.auteur_update, name="auteur_update"),
    path("auteurs/<int:id>/delete/", views.auteur_delete, name="auteur_delete"),
    path("categories/", views.categorie_list, name="categorie_list"),
    path("categories/ajouter/", views.categorie_create, name="categorie_create"),
    path("categories/<int:id>/delete/", views.categorie_delete, name="categorie_delete"),
]
