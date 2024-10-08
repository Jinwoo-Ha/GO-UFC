from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.utils import timezone
from .models import Post, Comment, Video, Fighter, Event, Match, Vote
from .forms import PostForm, CommentForm, SignUpForm, CustomAuthenticationForm
from django.db.models import Case, When
from .models import Video
from django.urls import reverse



def home(request):
    return render(request, 'home.html')

def video_list(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'new')
    
    if query:
        videos = Video.objects.filter(title__icontains=query)
    else:
        videos = Video.objects.all()
    
    if sort == 'new':
        videos = videos.order_by('-upload_date')
    elif sort == 'hot':
        videos = videos.order_by('-view_count')
    elif sort == 'recommend':
        videos = videos.order_by('-like_count')
    
    return render(request, 'video.html', {'videos': videos, 'query': query, 'sort': sort})

def community(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 15)
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

def fighter_detail(request, fighter_id):
    fighter = get_object_or_404(Fighter, id=fighter_id)
    return render(request, 'fighter_detail.html', {'fighter': fighter})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

# 새로 추가된 함수들

def upcoming_events(request):
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:5]
    
    for event in events:
        event.matches_list = event.matches.all()
        for match in event.matches_list:
            match.fighter1_votes = match.votes.filter(chosen_fighter=match.fighter1).count()
            match.fighter2_votes = match.votes.filter(chosen_fighter=match.fighter2).count()
    
    return render(request, 'upcoming.html', {'events': events})



@login_required(login_url='login')
def vote_match(request, match_id):
    if request.method == 'POST':
        match = get_object_or_404(Match, id=match_id)
        fighter_id = request.POST.get('vote')
        fighter = get_object_or_404(Fighter, id=fighter_id)
        
        vote, created = Vote.objects.update_or_create(
            user=request.user,
            match=match,
            defaults={'chosen_fighter': fighter}
        )
        
    return redirect('upcoming_events')


# 채팅방 기능 

@login_required(login_url='login')
def chatroom(request):
    return render(request, 'chatroom.html')


# 챔피언

from django.db.models import Case, When

def search_results(request):
    query = request.GET.get('q')
    fighters = Fighter.objects.filter(name__icontains=query) if query else None
    
    # 특정 ID의 파이터들만 가져오기
    selected_ids = [30, 35, 39, 44, 7, 8]
    popular_fighters = Fighter.objects.filter(id__in=selected_ids)

    # 체급 순서 정의
    weight_class_order = [
        'Flyweight', 'Bantamweight', 'Featherweight', 'Lightweight', 
        'Welterweight', 'Middleweight', 'Light Heavyweight', 'Heavyweight',
        "Women's Strawweight", "Women's Flyweight", "Women's Bantamweight", "Women's Featherweight"
    ]

    # Case-When expression으로 정렬
    weight_class_order_expression = Case(
        *[When(weight_class=class_name, then=pos) for pos, class_name in enumerate(weight_class_order)]
    )
    
    # 챔피언들 쿼리 및 정렬
    champions = Fighter.objects.filter(status='Champion').order_by(weight_class_order_expression)

    return render(request, 'search.html', {
        'fighters': fighters,
        'query': query,
        'popular_fighters': popular_fighters,
        'champions': champions
    })


