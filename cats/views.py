from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Breed, Cat


# Every view requires login, so anonymous users get sent to /accounts/login/
class CatList(LoginRequiredMixin, View):
    def get(self, request):
        ctx = {
            "breed_count": Breed.objects.count(),
            "cat_list": Cat.objects.all(),
        }
        return render(request, "cats/cat_list.html", ctx)


class BreedList(LoginRequiredMixin, View):
    def get(self, request):
        ctx = {"breed_list": Breed.objects.all()}
        return render(request, "cats/breed_list.html", ctx)


# Generic edit views look for cats/<model>_form.html and
# cats/<model>_confirm_delete.html by default
class BreedCreate(LoginRequiredMixin, CreateView):
    model = Breed
    fields = "__all__"
    success_url = reverse_lazy("cats:all")


class BreedUpdate(LoginRequiredMixin, UpdateView):
    model = Breed
    fields = "__all__"
    success_url = reverse_lazy("cats:all")


class BreedDelete(LoginRequiredMixin, DeleteView):
    model = Breed
    success_url = reverse_lazy("cats:all")


class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = "__all__"
    success_url = reverse_lazy("cats:all")


class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = "__all__"
    success_url = reverse_lazy("cats:all")


class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    success_url = reverse_lazy("cats:all")
