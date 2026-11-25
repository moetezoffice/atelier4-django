from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AuthorForm, BookForm, CategoryForm
from .models import Author, Book, Category


def livre_list(request):
    recherche = request.GET.get("q", "").strip()
    livres = Book.objects.filter(price__lt=50)
    if recherche:
        livres = livres.filter(title__icontains=recherche)
    livres = livres.order_by("-publication_date", "title")
    context = {
        "livres": livres,
        "titre_page": "Catalogue des livres",
        "recherche": recherche,
    }
    return render(request, "catalogue/livre_list.html", context)


def livre_detail(request, pk):
    livre = get_object_or_404(Book, pk=pk)
    context = {"livre": livre}
    return render(request, "catalogue/livre_detail.html", context)


def auteur_list(request):
    auteurs = Author.objects.all().order_by("last_name", "first_name")
    context = {"auteurs": auteurs}
    return render(request, "catalogue/auteur_list.html", context)


def auteur_detail(request, pk):
    auteur = get_object_or_404(Author, pk=pk)
    livres = auteur.books.all().order_by("title")
    context = {
        "auteur": auteur,
        "livres": livres,
        "nombre_livres": livres.count(),
    }
    return render(request, "catalogue/auteur_detail.html", context)


def categorie_list(request):
    categories = Category.objects.all().order_by("name")
    context = {"categories": categories}
    return render(request, "catalogue/categorie_list.html", context)


def livre_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            livre = form.save()
            messages.success(request, f"Le livre « {livre.title} » a été ajouté.")
            return redirect("catalogue:livre_detail", pk=livre.pk)
    else:
        form = BookForm()
    return render(
        request,
        "catalogue/livre_form.html",
        {"form": form, "titre_page": "Ajouter un livre"},
    )


def livre_update(request, id):
    livre = get_object_or_404(Book, pk=id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=livre)
        if form.is_valid():
            form.save()
            messages.success(request, f"Le livre « {livre.title} » a été modifié.")
            return redirect("catalogue:livre_detail", pk=livre.pk)
    else:
        form = BookForm(instance=livre)
    return render(
        request,
        "catalogue/livre_form.html",
        {"form": form, "titre_page": f"Modifier : {livre.title}"},
    )


def livre_delete(request, id):
    livre = get_object_or_404(Book, pk=id)
    if request.method == "POST":
        titre = livre.title
        livre.delete()
        messages.success(request, f"Le livre « {titre} » a été supprimé.")
        return redirect("catalogue:livre_list")
    return render(request, "catalogue/livre_confirm_delete.html", {"livre": livre})


def auteur_create(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            auteur = form.save()
            messages.success(request, f"L’auteur « {auteur} » a été ajouté.")
            return redirect("catalogue:auteur_detail", pk=auteur.pk)
    else:
        form = AuthorForm()
    return render(
        request,
        "catalogue/auteur_form.html",
        {"form": form, "titre_page": "Ajouter un auteur"},
    )


def auteur_update(request, id):
    auteur = get_object_or_404(Author, pk=id)
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=auteur)
        if form.is_valid():
            form.save()
            messages.success(request, f"L’auteur « {auteur} » a été modifié.")
            return redirect("catalogue:auteur_detail", pk=auteur.pk)
    else:
        form = AuthorForm(instance=auteur)
    return render(
        request,
        "catalogue/auteur_form.html",
        {"form": form, "titre_page": f"Modifier : {auteur}"},
    )


def auteur_delete(request, id):
    auteur = get_object_or_404(Author, pk=id)
    nombre_livres = auteur.books.count()
    if request.method == "POST":
        nom = str(auteur)
        auteur.delete()
        messages.success(
            request,
            f"L’auteur « {nom} » et ses {nombre_livres} livre(s) ont été supprimés.",
        )
        return redirect("catalogue:auteur_list")
    return render(
        request,
        "catalogue/auteur_confirm_delete.html",
        {"auteur": auteur, "nombre_livres": nombre_livres},
    )


def categorie_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            categorie = form.save()
            messages.success(request, f"La catégorie « {categorie.name} » a été ajoutée.")
            return redirect("catalogue:categorie_list")
    else:
        form = CategoryForm()
    return render(
        request,
        "catalogue/categorie_form.html",
        {"form": form, "titre_page": "Ajouter une catégorie"},
    )


def categorie_delete(request, id):
    categorie = get_object_or_404(Category, pk=id)
    if request.method == "POST":
        nom = categorie.name
        try:
            categorie.delete()
        except ProtectedError:
            messages.error(
                request,
                f"La catégorie « {nom} » ne peut pas être supprimée car elle contient des livres.",
            )
        else:
            messages.success(request, f"La catégorie « {nom} » a été supprimée.")
        return redirect("catalogue:categorie_list")
    return render(
        request,
        "catalogue/categorie_confirm_delete.html",
        {"categorie": categorie, "nombre_livres": categorie.books.count()},
    )
