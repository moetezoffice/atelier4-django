# Atelier 04 — Explication et réponses

Cette réalisation prolonge l’application `catalogue` des ateliers précédents. Les formulaires sont traités dans l’application, et les modèles `Author`, `Book` et `Category` restent la source des règles de données.

## Étape 1 — Comprendre le cycle d’un formulaire

Une requête `GET` affiche la page. Pour une création, la vue construit un formulaire vide ; pour une modification, elle lui donne l’objet existant avec `instance=...` afin de préremplir les champs.

Une requête `POST` contient les valeurs saisies. Le formulaire est lié à ces valeurs et `is_valid()` vérifie les types et règles Django. Si la saisie est invalide, la même page est renvoyée avec les valeurs et les erreurs. Si elle est valide, `save()` écrit en base puis la vue redirige vers une autre page (Post/Redirect/Get).

## Étape 2 — Définir les formulaires

`catalogue/forms.py` contient trois `ModelForm`. Chaque classe `Meta` nomme le modèle et liste uniquement les champs que l’utilisateur peut modifier. Django génère les champs HTML et réutilise les validations du modèle, dont les champs obligatoires et l’unicité de l’adresse e-mail et du nom de catégorie.

`BookForm.clean_price()` refuse les montants inférieurs ou égaux à zéro. `clean_publication_date()` refuse une date après la date locale d’aujourd’hui. Le widget HTML `type=date` affiche un sélecteur de date et le format `%Y-%m-%d` permet de recharger la valeur lors de la modification.

`joined_date` ne figure pas dans `AuthorForm` car `auto_now_add=True` fait attribuer cette date automatiquement à la création. Ce n’est pas une donnée à saisir ou à modifier par le visiteur.

## Étape 3 — Traiter la création, la modification et la suppression

Les vues `livre_create`, `livre_update` et `livre_delete` suivent le cycle décrit plus haut. La vue de modification passe toujours `instance=livre` au formulaire POST ; sans cela, `save()` créerait un nouvel enregistrement.

Les vues `auteur_create` et `auteur_update` réutilisent `AuthorForm`. La vue `auteur_delete` calcule le nombre de livres avant suppression et l’affiche sur la page de confirmation. Le modèle utilise `on_delete=CASCADE` : confirmer la suppression de l’auteur efface aussi ses livres.

La création de catégorie utilise `CategoryForm`. Pour le bonus de suppression, la vue capture `ProtectedError`, provoquée par `on_delete=PROTECT` lorsqu’un livre utilise encore la catégorie. Au lieu d’une erreur serveur, l’utilisateur revient à la liste avec un message explicatif.

Toutes les suppressions effectives sont limitées à une requête `POST`. Une requête `GET` affiche seulement la confirmation : suivre un lien ou précharger une page ne peut donc pas effacer de données.

## Étape 4 — Déclarer les URL

`catalogue/urls.py` associe un chemin lisible à chaque vue. Le nom de route (`livre_create`, par exemple) sert aux templates via `{% url ... %}` et aux vues via `redirect(...)`. Les identifiants d’objet passent dans le chemin pour les opérations sur une fiche existante.

## Étape 5 — Créer les pages

Les templates de formulaire partagent le même motif : `method="post"`, `{% csrf_token %}`, rendu du formulaire et bouton d’enregistrement. `csrf_token` prouve que le POST vient d’une page fournie par l’application ; sans lui, le middleware CSRF répond normalement par HTTP 403.

Les pages de confirmation demandent une seconde action explicite, avec un formulaire POST. `base.html` affiche les messages à usage unique après redirection. Les vues ajoutent ces messages avec `messages.success()` ou `messages.error()`.

## Étape 6 — Rechercher un livre

Le formulaire de recherche utilise `GET`, car il ne modifie aucune donnée. Django reçoit le terme dans `request.GET["q"]`, filtre le titre avec `icontains` (recherche sans distinction de casse), puis renvoie `recherche` au template afin de conserver le texte saisi. La liste garde le filtre préexistant de l’atelier 03 sur les livres à moins de 50 TND.

## Réponses aux questions de réflexion

1. **Que se passe-t-il sans `{% csrf_token %}` ?** Le middleware CSRF rejette le POST et renvoie une réponse 403. Le jeton empêche un autre site de faire soumettre à l’insu de l’utilisateur une action avec sa session.
2. **Pourquoi rediriger après un POST réussi ?** Le navigateur affiche ensuite une page GET ; actualiser cette page ne renvoie pas le POST, ce qui évite la répétition accidentelle d’une création ou d’une modification.
3. **Pourquoi supprimer avec POST ?** La suppression change l’état des données. Un lien déclenche un GET, que les robots, préchargements ou outils de navigation peuvent visiter sans intention de confirmer une suppression.

## Exercice d’application et règles de suppression

- **Ajouter une catégorie :** `CategoryForm`, `categorie_create`, sa route et `categorie_form.html` réalisent l’ajout. La contrainte `unique=True` sur `Category.name` empêche les doublons.
- **Modifier un auteur :** `auteur_update` réutilise `AuthorForm` avec `instance=auteur` et est accessible depuis le détail de l’auteur.
- **Supprimer un auteur :** la confirmation annonce le nombre de livres qui seront effacés par `CASCADE`.
- **Bonus catégorie :** si la catégorie est référencée par des livres, `PROTECT` empêche sa suppression ; `ProtectedError` est interceptée et affichée sous forme de message.

## Pour lancer l’application

Depuis le dossier `mysite`, activez l’environnement virtuel puis exécutez `python manage.py runserver`. Consultez `/catalogue/livres/`, `/catalogue/auteurs/` et `/catalogue/categories/`. Pour vérifier à la main, essayez un prix négatif, une date future, un e-mail déjà utilisé, une recherche par titre et la suppression d’une catégorie qui possède des livres.
