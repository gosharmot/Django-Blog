from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.views.generic import View
from django.views.generic.edit import FormView

from django.db import transaction

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Post, Tag
from .utils import *
from .forms import TagForm, PostForm, CommentForm, ProfileForm, UserForm



class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = '/login/'
    template_name = 'blog/register.html'

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegisterFormView, self).form_invalid(form)


class LoginFormView(LoginView):
    form_class = AuthenticationForm
    success_url = '/'
    template_name = 'blog/login.html'

    def get_success_url(self):
        return self.success_url


class LogOutView(LogoutView):
    next_page = '/'


def home_page_view(request):
    return render(request, 'blog/home_page.html')


def posts_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/posts_list.html', context={'posts': posts})


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'
    model_form = CommentForm


class TagsDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tags_detail.html'
    model_form = TagForm


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = PostForm
    template = 'blog/post_create.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = TagForm
    template = 'blog/tag_create.html'


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/update.html'


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/update.html'


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'blog/delete.html'
    redirect_url = 'posts_list_url'


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/delete.html'
    redirect_url = 'tags_list_url'


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return render(request, 'blog/profile.html', context={
                'user_form': user_form,
                'profile_form': profile_form
            })
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'blog/profile.html', context={
        'user_form': user_form,
        'profile_form': profile_form
    })
