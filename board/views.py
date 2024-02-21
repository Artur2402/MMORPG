from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse

from .models import Post, Response
from .filters import PostFilter
from .forms import PostForm, ResponsesForm, RespondForm
from .tasks import respond_send_email, respond_accept_send_email


class Index(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'index.html'


class Search(ListView):
    model = Post
    context_object_name = 'search'
    template_name = 'search.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Response.objects.filter(author_id=self.request.user.id).filter(post_id=self.kwargs.get('pk')):
            context['respond'] = "Откликнулся"
        elif self.request.user == Post.objects.get(pk=self.kwargs.get('pk')).author:
            context['respond'] = "Мое_объявление"
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm('board.add_post'):
            return HttpResponseRedirect(reverse('account_profile'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = User.objects.get(id=self.request.user.id)
        post.save()
        return redirect(f'/post/{post.id}')


class EditPost(PermissionRequiredMixin, UpdateView):
    permission_required = 'board.change_post'
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    def dispatch(self, request, *args, **kwargs):
        author = Post.objects.get(pk=self.kwargs.get('pk')).author.username
        if self.request.user.username == 'admin' or self.request.user.username == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse('Редактировать пост может только его автор!!!')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('post/' + str(self.kwargs.get('pk')))


class DeletePost(PermissionRequiredMixin, DeleteView):
    permission_required = 'board.delete_post'
    model = Post
    template_name = 'post_delete.html'
    success_url = '/index'

    def dispatch(self, request, *args, **kwargs):
        author = Post.objects.get(pk=self.kwargs.get('pk')).author.username
        if self.request.user.username == 'admin' or self.request.user.username == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse('Удалить пост может только его автор!!!')


title = str("")


class Responses(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'responses.html'
    context_object_name = 'responses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        global title

        if self.kwargs.get('pk') and Post.objects.filter(id=self.kwargs.get('pk')).exists():
            title = str(Post.objects.get(id=self.kwargs.get('pk')).title)
            print(title)
        context['form'] = ResponsesForm(self.request.user, initial={'title': title})
        context['title'] = title
        if title:
            post_id = Post.objects.get(title=title)
            context['filter_responses'] = list(Response.objects.filter(post_id=post_id).order_by('-dateCreation'))
            context['response_post_id'] = post_id.id
        else:
            context['filter_responses'] = list(Response.objects.filter(post_id__author_id=self.request.user).order_by('-dateCreation'))
        context['myresponses'] = list(Response.objects.filter(author_id=self.request.user).order_by('-dateCreation'))
        return context

    def post(self, request, *args, **kwargs):
        global title
        title = self.request.POST.get('title')
        if self.kwargs.get('pk'):
            return HttpResponseRedirect('/responses')
        return self.get(request, *args, **kwargs)


class Respond(LoginRequiredMixin, CreateView):
    model = Response
    template_name = 'respond.html'
    form_class = RespondForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        respond = form.save(commit=False)
        respond.author = User.objects.get(id=self.request.user.id)
        respond.post = Post.objects.get(id=self.kwargs.get('pk'))
        respond.save()
        respond_send_email.delay(respond_id=respond.id)
        return redirect(f'/post/{self.kwargs.get("pk")}')


@login_required
def response_accept(request, **kwargs):
    if request.user.is_authenticated:
        response = Response.objects.get(id=kwargs.get('pk'))
        response.status = 'A'
        response.save()
        respond_accept_send_email.delay(response_id=response.id)
        return HttpResponseRedirect('/responses')
    else:
        return HttpResponseRedirect('/accounts/login')


@login_required
def response_reject(request, **kwargs):
    if request.user.is_authenticated:
        response = Response.objects.get(id=kwargs.get('pk'))
        response.status = 'D'
        response.save()
        return HttpResponseRedirect('/responses')
    else:
        return HttpResponseRedirect('/accounts/login')