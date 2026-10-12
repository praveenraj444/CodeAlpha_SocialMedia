from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q

from .models import Post, Profile, Like, Comment
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    PostForm,
    CommentForm,
)
from .utils import search_youtube_videos


# ─────────────────────────────────────────────────────────
# AUTHENTICATION VIEWS
# ─────────────────────────────────────────────────────────

def register_view(request):
    """User registration page."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()

    return render(request, 'social_app/register.html', {'form': form})


def login_view(request):
    """User login page."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'social_app/login.html')


def logout_view(request):
    """User logout."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# ─────────────────────────────────────────────────────────
# HOME / FEED
# ─────────────────────────────────────────────────────────

@login_required
def home_view(request):
    """Home feed — all posts (newest first)."""
    posts = Post.objects.select_related('user', 'user__profile').prefetch_related(
        'likes', 'comments__user'
    ).all()

    # User-liked posts list (heart fill panna)
    user_liked_ids = list(
        Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    )

    context = {
        'posts': posts,
        'user_liked_ids': user_liked_ids,
    }
    return render(request, 'social_app/home.html', context)


# ─────────────────────────────────────────────────────────
# PROFILE VIEWS
# ─────────────────────────────────────────────────────────

@login_required
def profile_view(request):
    """Logged-in user-oda own profile."""
    user_posts = Post.objects.filter(user=request.user).order_by('-created_at')
    profile = request.user.profile

    context = {
        'profile_user': request.user,
        'profile': profile,
        'posts': user_posts,
        'post_count': user_posts.count(),
        'is_own_profile': True,
    }
    return render(request, 'social_app/profile.html', context)


@login_required
def user_profile_view(request, username):
    """Other user-oda profile view."""
    profile_user = get_object_or_404(User, username=username)
    profile = profile_user.profile
    user_posts = Post.objects.filter(user=profile_user).order_by('-created_at')

    context = {
        'profile_user': profile_user,
        'profile': profile,
        'posts': user_posts,
        'post_count': user_posts.count(),
        'is_own_profile': (profile_user == request.user),
    }
    return render(request, 'social_app/profile.html', context)


@login_required
def edit_profile_view(request):
    """Profile edit page."""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'social_app/edit_profile.html', context)


# ─────────────────────────────────────────────────────────
# POST VIEWS
# ─────────────────────────────────────────────────────────

@login_required
def create_post_view(request):
    """Create new post (image / YouTube / Instagram)."""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('home')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = PostForm()

    return render(request, 'social_app/create_post.html', {'form': form})


@login_required
def delete_post_view(request, post_id):
    """Delete own post."""
    post = get_object_or_404(Post, id=post_id)

    # Only post owner can delete
    if post.user != request.user:
        messages.error(request, "You can only delete your own posts.")
        return redirect('home')

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted.")
        return redirect('home')

    # GET-ku confirmation page (optional — naama direct POST pannuvom)
    return render(request, 'social_app/delete_post_confirm.html', {'post': post})


# ─────────────────────────────────────────────────────────
# LIKE / UNLIKE (AJAX)
# ─────────────────────────────────────────────────────────

@login_required
@require_POST
def like_post_view(request, post_id):
    """Like / Unlike toggle (AJAX)."""
    post = get_object_or_404(Post, id=post_id)

    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        # Already liked → unlike
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'liked': liked,
        'total_likes': post.total_likes(),
    })


# ─────────────────────────────────────────────────────────
# COMMENT (AJAX)
# ─────────────────────────────────────────────────────────

@login_required
@require_POST
def add_comment_view(request, post_id):
    """Add comment (AJAX real-time)."""
    post = get_object_or_404(Post, id=post_id)
    text = request.POST.get('text', '').strip()

    if not text:
        return JsonResponse({'error': 'Comment cannot be empty.'}, status=400)

    if len(text) > 300:
        return JsonResponse({'error': 'Comment too long (max 300 chars).'}, status=400)

    comment = Comment.objects.create(
        user=request.user,
        post=post,
        text=text
    )

    return JsonResponse({
        'success': True,
        'comment_id': comment.id,
        'username': comment.user.username,
        'user_profile_pic': comment.user.profile.profile_pic.url if comment.user.profile.profile_pic else '',
        'text': comment.text,
        'created_at': comment.created_at.strftime('%b %d, %Y'),
        'total_comments': post.total_comments(),
    })


# ─────────────────────────────────────────────────────────
# YOUTUBE SEARCH (AJAX)
# ─────────────────────────────────────────────────────────

@login_required
def youtube_search_view(request):
    """YouTube search — AJAX endpoint."""
    query = request.GET.get('q', '').strip()

    if not query:
        return JsonResponse({'error': 'Please enter a search term.'}, status=400)

    if len(query) > 100:
        return JsonResponse({'error': 'Search term too long.'}, status=400)

    results = search_youtube_videos(query, max_results=8)

    return JsonResponse({
        'query': query,
        'count': len(results),
        'results': results,
    })