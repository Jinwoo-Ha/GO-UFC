from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Video
from .forms import PostForm, CommentForm
from .models import Fighter


def home(request):
    return render(request, 'home.html')


def video_list(request):
    videos = Video.objects.all().order_by('-created_at')[:15]
    return render(request, 'video.html', {'videos': videos})

def community(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 15)  # 15 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'community.html', {'posts': page_obj})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('community')

@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', pk=pk)

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form, 'post': post})


def search_results(request):
    query = request.GET.get('q')
    fighters = Fighter.objects.filter(name__icontains=query) if query else None
    
    # 인기 있는 UFC 파이터 목록 (예시로 상위 6명 가져오기)
    popular_fighters = Fighter.objects.all()[:6]
    
    return render(request, 'search.html', {
        'fighters': fighters,
        'query': query,
        'popular_fighters': popular_fighters
    })

def fighter_detail(request, fighter_id):
    fighter = get_object_or_404(Fighter, id=fighter_id)
    return render(request, 'fighter_detail.html', {'fighter': fighter})

