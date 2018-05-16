from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from taggit.models import Tag
from .models import Post, Category

from .forms import PostForm, CategoryForm


# Create your views here.
def blog_posts(request):

    ctx = {
            "page": "posts"
    }

    posts = Post.objects.filter(published_date__lte=timezone.now()
                                ).order_by('-published_date')

    tags = Tag.objects.all()

    categories = []

    for each_tag in tags:
        categories.append(each_tag)

    ctx['posts'] = posts
    ctx['categories'] = categories
    
    return render(request, "blog/blog_posts.html", ctx)

# Create your views here.
def view_category_posts(request, pk):

    category = get_object_or_404(Tag, pk=pk)

    ctx = {
            "page": "posts"
    }

    posts = Post.objects.all()

    posts = posts.filter(category__in=[category]).order_by('-published_date')

    tags = Tag.objects.all()

    categories = []

    for each_tag in tags:
        categories.append(each_tag)

    ctx['posts'] = posts

    ctx['categories'] = categories
    
    return render(request, "blog/posts_under_category.html", ctx)

@login_required
def add_post(request):

    ctx = {
        "page": "posts"
    }

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            #set commit to false so you can add extra data before saving
            post = form.save(commit=False)

            #add more data before saving
            post.author = request.user
            post.published_date = timezone.now()

            post.save()

            # Without this next line the tags won't be saved.
            form.save_m2m()

            return redirect('blog-view-posts')
    else:

        form = PostForm()
        ctx['form'] = form

    return render(request, "blog/add_blog_post.html", ctx)

@login_required
def add_category(request):

    ctx = {
        "page": "posts"
    }

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            #set commit to false so you can add extra data before saving
            category = form.save(commit=False)

            category.save()

            return redirect('blog-view-posts')
    else:

        form = CategoryForm()
        ctx['form'] = form

    return render(request, "blog/add_category.html", ctx)

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return HttpResponseForbidden()

    ctx = {
        "page": "posts"
    }

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)

            post.save()

            # Without this next line the tags won't be saved.
            form.save_m2m()

            return redirect('view-post-details', pk=post.pk)
    else:

        form = PostForm(instance=post)

        ctx['form'] = form

    return render(request, 'blog/edit_blog_post.html', ctx)

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return HttpResponseForbidden()

    post.delete()

    ctx = {
        "page": "posts"
    }

    if post is None:
        ctx['message'] = "Sorry post does not exist"

    return redirect('blog-view-posts')

def post_details(request, pk):

    ctx = {
            "page": "posts"
    }

    post = get_object_or_404(Post, pk=pk)

    ctx['post'] = post

    return render(request, "blog/view_post.html", ctx)