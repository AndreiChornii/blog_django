from django.shortcuts import render, redirect

from .models import Blog, Post
from .forms import BlogForm, PostForm

def blogs(request):
    blogs = Blog.objects.order_by("date_added")
    context = {"blogs": blogs}
    return render(request, 'blogs/blogs.html', context)

def new_blog(request):
    if request.method != 'POST':
        form = BlogForm()
    else:
        form = BlogForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:blogs')
        
    context = {'form': form}
    return render(request, 'blogs/new_blog.html', context)

def blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    posts = blog.post_set.order_by('-date_added')
    context = {'blog': blog, 'posts': posts}
    return render(request, 'blogs/blog.html', context)

def new_post(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.blog = blog
            new_post.save()
            return redirect('blogs:blog', blog_id=blog_id)
    context = {'blog': blog, 'form': form}
    return render(request, 'blogs/new_post.html', context)

def edit_blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)

    if request.method != 'POST':
        form = BlogForm(instance=blog)
    else:
        form = BlogForm(instance=blog, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:blogs')
    context = {'blog': blog, 'form': form}
    return render(request, 'blogs/edit_blog.html', context)

def delete_blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    blog.delete()
    return redirect('blogs:blogs')

def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    blog = post.blog

    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:blog', blog_id=blog.id)
    context = {'post': post, 'blog': blog, 'form': form}
    return render(request,'blogs/edit_blog.html', context)

def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    blog = post.blog
    post.delete()
    return redirect('blogs:blog', blog_id=blog.id)
