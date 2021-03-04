from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from PIL import Image
from .models import *


class ObjectDetailMixin:
    model = None
    template = None
    model_form = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        form = self.model_form()
        comments = Comment.objects.filter(slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj, 'form': form, 'comments': comments})

    def post(self, request, slug):
        username = request.user.username
        obj = get_object_or_404(self.model, slug__iexact=slug)
        bound_form = self.model_form(request.POST)
        comments = Comment.objects.filter(slug__iexact=slug)
        user = User.objects.get(username=username)



        if bound_form.is_valid():
            new_obj = bound_form.save()
            new_obj.username = username
            new_obj.slug = slug
            user.profile.avatar.open()
            new_obj.avatar = user.profile.avatar.open()
            new_obj.save()
            form = self.model_form()
            return render(request, self.template, context={self.model.__name__.lower(): obj, 'form': form, 'comments': comments})
        return render(request, self.template, context={self.model.__name__.lower(): obj, 'form': form, 'comments': comments})


class ObjectCreateMixin:
    model_form = None
    template = None

    def get(self, request):
        form = self.model_form()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bound_form = self.model_form(request.POST)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form})


class ObjectUpdateMixin:
    model = None
    model_form = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(instance=obj)
        obj_name = self.model.__name__
        return render(request, self.template, context={'form': bound_form, 'obj': obj, 'title': obj_name})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST, instance=obj)
        obj_name = self.model.__name__

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form, 'obj': obj, 'title': obj_name})


class ObjectDeleteMixin:
    model = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj_name = self.model.__name__
        return render(request, self.template, context={'title': obj_name, 'obj': obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj_name = self.model.__name__
        obj.delete()
        return redirect(reverse(self.redirect_url))
