from django.shortcuts import render, redirect
from .models import Blog, Post
from .forms import CreateBlogForm, CreatePostForm


def home_page(request):
    if request.user.is_authenticated:
        blogs = Blog.objects.filter(owner_id=request.user.id).order_by('-created_at')
        return render(request, 'blogs/index.html', {'blogs': blogs})
    else:
        return redirect('/auth/login/')


def create_blog_page(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            form = CreateBlogForm()
            return render(request, 'blogs/create-blog.html', {'form': form})
        if request.method == 'POST':
            form = CreateBlogForm(request.POST)
            if form.is_valid():
                title = form.data.get('title')
                description = form.data.get('description')
                blog = Blog(title=title, description=description, owner_id=request.user.id)
                blog.save()
                return redirect('/')
            else:
                return render(request, 'blogs/create-blog.html', {'form': form})
    else:
        return redirect('/auth/login/')


def blog_details_page(request, pk):
    if request.method == 'GET':
        form = CreatePostForm()
        blog = Blog.objects.get(id=pk)
        posts = Post.objects.filter(blog_id=pk)
        return render(request, 'blogs/blog-details.html', {'blog': blog, 'user': request.user, 'form': form,
                                                           'posts': posts})


def delete_blog_page(request, pk):
    if request.method == 'GET':
        blog = Blog.objects.get(id=pk)
        if request.user.id == blog.owner.id:
            blog.delete()
            return redirect('/')
        return redirect('/')


def create_blogs_post(request, pk):
    if request.method == 'POST':
        blog = Blog.objects.get(id=pk)
        if request.user.id == blog.owner_id:
            form = CreatePostForm(request.POST)
            if form.is_valid():
                title = form.data.get('title')
                content = form.data.get('content')
                post = Post(title=title, content=content, blog_id=blog.id)
                post.save()
                return redirect('/blogs/' + str(blog.id) + '/')
            else:
                return render(request, 'blogs/blog-details.html', {'blog': blog, 'user': request.user, 'form': form})
        else:
            return redirect('/')


def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    if post.blog.owner.id == request.user.id:
        post.delete()
        return redirect('/blogs/' + str(post.blog.id) + '/')
    else:
        return redirect('/')


def post_details(request, pk):
    post = Post.objects.get(id=pk)
    return render(request, 'blogs/post-details.html', {'post': post})
