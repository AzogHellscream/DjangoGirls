from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.template.defaultfilters import slugify
from .models import Post, PostViews
from .forms import PostForm, LoginForm, UserRegistrationForm
import re
from taggit.models import Tag
from collections import Counter
from rest_framework import generics
from .serializers import PostSerializer

# Create your views here.



def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.pk is not None:
        viewed_post = PostViews(user=request.user, post=post)
        viewed_post.save()
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.slug = slugify(post.title)
            post.save()
            text = form.cleaned_data['text']
            # This construction get hashtags from text, then put them in DataBase without #
            hashtags = (n.replace('#', '') for n in list(set([re.sub(r"(\W+)$", "", j) for j in set([i for i in text.split() if i.startswith("#")])])))
            post.tags.add(*[item for item in hashtags])
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def user_login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            login_user = authenticate(username=username, password=password)
            if login_user:
                login(request, login_user)
                return redirect('post_list', permanent=True)
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid() and user_form.cleaned_data['redirect_checkbox']:
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password'],
                                    )
            login(request, new_user)
            return redirect('post_list', permanent=True)
        elif user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'blog/register_done_need_login.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'user_form': user_form})


def top_ten_tags(request):
    used_tags = []
    # Cycle gives list of all used tags in var 'used_tags'
    for post in Post.objects.all():
        for tag in Post.objects.get(title=post).tags.all():
            used_tags.append(tag)

    unsorted_values = Counter(used_tags)  # Here makes dict {Tag: Number of uses}
    sorted_values = sorted(unsorted_values.values(), reverse=True)  # Sort the values
    sorted_dict = {}

    for i in sorted_values[:9]:  # :9 means that we get top-10 tags
        for k in unsorted_values.keys():
            if unsorted_values[k] == i and len(sorted_dict) < 10:
                sorted_dict[k] = unsorted_values[k]
    return render(request, 'blog/top_ten_tags.html', {'sorted_dict': sorted_dict})


class PostAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
