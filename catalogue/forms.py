from django import forms
from django.utils import timezone

from .models import Author, Book, Category


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "summary", "publication_date", "price", "author", "category"]
        widgets = {
            "summary": forms.Textarea(attrs={"rows": 4}),
            "publication_date": forms.DateInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            ),
        }

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price <= 0:
            raise forms.ValidationError("Le prix doit être strictement positif.")
        return price

    def clean_publication_date(self):
        publication_date = self.cleaned_data["publication_date"]
        if publication_date > timezone.localdate():
            raise forms.ValidationError("La date de publication ne peut pas être dans le futur.")
        return publication_date


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["first_name", "last_name", "email"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}
