from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
# Create your views here.
from .models import Post, Category, ExtraImage, IpModel, Comment, SocialName, About
from .forms import CreatePostForm, ExtraImageForm, SearchForm, CreateCategoryForm, UserCommentForm, GuestCommentForm
import time


# Posts ------------------------------------------------------------------------------
class PostsView(ListView):
    paginate_by = 4
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(show=True)


# likes ----------------------------------------------------------------------------
@login_required()
def like_post(request, slug):
    post = Post.objects.get(slug=slug)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('blog:detail_post', args=[str(slug)]))


# Detail Posts ------------------------------------------------------------------------------
def detail_post(request, post_slug):
    post = Post.objects.get(slug=post_slug)
    eis = post.extraimage_set.all()
    comments = Comment.objects.filter(post=post.pk, is_active=True)

    total_likes = post.total_likes()
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True

    ip = get_ip(request)
    s = post_slug
    results = IpModel.objects.filter(ip=ip, post=s)
    if results.exists():
        pass
    else:
        IpModel.objects.create(ip=ip, post=s)
        post.views = post.views + 1
        post.save()

    initial = {'post': post.id}
    if request.user.is_authenticated:
        initial['name'] = request.user.username
        form_class = UserCommentForm
    else:
        form_class = GuestCommentForm

    form = form_class(initial=initial)
    if request.method == "POST":
        c_form = form_class(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.success(request, 'Comment has added')
        else:
            form = c_form
    context = {'post': post, 'eis': eis, 'form': form, 'comments': comments, 'liked': liked, 'total_likes':total_likes}
    return render(request, 'blog/detail.html', context)


# Get user ip --------------------------------------------------------------------------
def get_ip(request):
    address = request.META.get('HTTP_X_FORWARDED_FOR')
    if address:
        ip = address.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Create Posts ------------------------------------------------------------------------------
@login_required()
def create_post(request):
    form = CreatePostForm()
    formset = ExtraImageForm()
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            formset = ExtraImageForm(request.POST, request.FILES, instance=post)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'Post has created!')
                return HttpResponseRedirect(reverse('blog:create_post'))
        else:
            messages.warning(request, 'Post has not created try again')
    else:
        form = CreatePostForm(initial={'author': request.user.pk})
        formset = ExtraImageForm()
    context = {'formset': formset, 'form': form, 'save': 'Create'}
    return render(request, 'blog/create_post.html', context)


# Update Posts ------------------------------------------------------------------------------
@login_required()
def update_post(request, post_slug):
    post = Post.objects.get(slug=post_slug)
    form = CreatePostForm(instance=post)
    formset = ExtraImageForm(instance=post)
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            formset = ExtraImageForm(request.POST, request.FILES, instance=post)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'Post has updated!')
                return HttpResponseRedirect(reverse('blog:user_detail_post', kwargs={'post_slug': request.POST.get('slug')}))
        else:
            messages.warning(request, 'Post has not updated try again')
    else:
        form = CreatePostForm(instance=post)
        formset = ExtraImageForm(instance=post)
    context = {'formset': formset, 'form': form, 'save': 'Update', 'post': post}
    return render(request, 'blog/create_post.html', context)


# Detele Posts ------------------------------------------------------------------------------
class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'
    success_message = 'Post has deleted!'

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        success_url = reverse_lazy('blog:user_posts', kwargs={'pk':self.request.user.pk})
        return success_url

    def get_context_data(self, **kwargs):
        context = DetailView.get_context_data(self, **kwargs)
        post = Post.objects.get(slug=self.kwargs['post_slug'])
        context['eis'] = post.extraimage_set.all()
        return context


# User Posts ------------------------------------------------------------------------------
class UserPosts(LoginRequiredMixin, ListView):
    paginate_by = 4
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        posts = Post.objects.filter(author=self.request.user.pk)
        return posts


# User detail Post ------------------------------------------------------------------------------
@login_required()
def user_detail_post(request, post_slug):
    post = Post.objects.get(slug=post_slug)
    eis = post.extraimage_set.all()
    comments = Comment.objects.filter(post=post.pk)
    context = {'post': post, 'comments': comments, 'eis': eis}
    return render(request, 'blog/detail_user_post.html', context)


@login_required()
def delete_commet(request, pk):
    comment = Comment.objects.get(pk=pk)
    post = Post.objects.get(comment=comment)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment has removed')
        return HttpResponseRedirect(reverse('blog:user_detail_post', kwargs={'post_slug': post.slug}))
    else:
        context = {'comment': comment}
        return render(request, 'blog/delete_user_comment.html', context)
    
    
# Categories --------------------------------------------------------------------
def categories_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'blog/categories.html', context)


# By category ---------------------------------------------------------------------
class ByCategory(ListView):
    paginate_by = 4
    template_name = 'blog/by_category.html'
    context_object_name = 'posts'

    def get_queryset(self):
        post = Post.objects.filter(category__slug=self.kwargs['category_slug']).filter(show=True)
        return post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['current_category'] = Category.objects.get(slug=self.kwargs['category_slug'])
        return context


# Search ----------------------------------------------------------------------------------
class SearchView(ListView):
    paginate_by = 4
    template_name = 'blog/search_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        q = self.request.GET.get('q')
        post = Post.objects.get(title__icontains=q)
        return post
    
    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['keyword'] = self.request.GET.get('q')
        return context


# Create Category ------------------------------------------------------------------
class CreateCategoryView(LoginRequiredMixin, FormView):
    form_class = CreateCategoryForm
    template_name = 'blog/create_category.html'
    success_message = 'Category has created'
    success_url = reverse_lazy('blog:create_category')

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.success_url
        
    def form_valid(self, form):
        form.save()
        return FormView.form_valid(self, form)



# Social links ---------------------------------------------------------------------
class AboutView(TemplateView):
    template_name = 'blog/about.html'
    
    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context['sociallinks'] = SocialName.objects.all()
        about = About.objects.get(active=True)
        if about:
            context['about'] = about

        return context