from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from . forms import CustomUserCreationForm
from django.db.models import Q
from . models import *
from . forms import *

# Create your views here.

#User Register and Login and Logout Views

#register view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})



#login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('post_list')
    return render(request, 'users/login.html')



#logout view
def user_logout(request):
    logout(request)
    return redirect('post_list')


# --------------------------------- # ------------------ # -------------------------------- #


#Post & Comment Views

#post creating view
@login_required
def create_post(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form ,'categories': categories})



#post list view
def post_list(request):
    query = request.GET.get('q', '')
    posts = Post.objects.all().order_by('-created_at')
    if query:
        posts =  posts.filter(
            Q(title__icontains=query) | Q(category__name__icontains=query) | Q(content__icontains=query) | Q(author__username__icontains=query)
        )
    return render(request, 'posts/post_list.html', {'posts': posts})




#post detail view
@login_required
def post_detail(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments, 'form': form})




#post update view
@login_required
def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
        else:
            print(form.errors)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/update_post.html', {'form': form, 'post': post})




#post delete view
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'posts/delete_post.html', {'post': post})




#comment delete view
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', post_id=comment.post.id)
    return render(request, 'posts/delete_comment.html', {'comment': comment})
