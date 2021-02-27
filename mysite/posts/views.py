from django.shortcuts import render, redirect, get_object_or_404
from .models import Posts
from .forms import PostsForm
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, UpdateView


class PostDetailView(DetailView):
    model = Posts
    template_name = 'posts/detail.html'
    context_object_name = 'posts'


class PostUpdateView(UpdateView):
    model = Posts
    template_name = 'posts/update.html'
    form_class = PostsForm


@login_required(login_url='allauth:login page')
def index(request):
    posts = Posts.objects.all()
    return render(request, 'posts/index.html', {'posts' : posts})


@login_required(login_url='allauth:login page')
def new_post(request):
    error = ''
    if request.method == 'POST':
        form = PostsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('successful new request')
        else:
            error = 'Неверное заполнение формы'
    form = PostsForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'posts/new_post.html', data)


@login_required(login_url='allauth:login page')
def successful_new_request(request):
    return render(request, 'posts/new_post_success.html')


@login_required(login_url='allauth:login page')
def my_posts(request):
    posts = Posts.objects.all()
    return render(request, 'posts/my_posts.html', {'posts': posts, 'order': [1, 1, 1, 0, 0], 'o': 3,
                                                   'do': [1, 1, 0, 0, 0], 'd': 2})


@login_required(login_url='allauth:login page')
def personal_account(request):
    return render(request, 'posts/personal_account.html', {'order': [1, 1, 1, 0, 0], 'o': 3,
                                                           'do': [1, 1, 0, 0, 0], 'd': 2})
