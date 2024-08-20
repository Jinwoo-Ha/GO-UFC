from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    youtube_id = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
class Fighter(models.Model):
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, blank=True, null=True)
    weight_class = models.CharField(max_length=50)
    record = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='fighter_photos/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    hometown = models.CharField(max_length=30, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    height = models.CharField(max_length=10, null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    career_highlights = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

# 새로 추가된 모델들

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class Match(models.Model):
    event = models.ForeignKey(Event, related_name='matches', on_delete=models.CASCADE)
    fighter1 = models.ForeignKey(Fighter, related_name='matches_as_fighter1', on_delete=models.CASCADE)
    fighter2 = models.ForeignKey(Fighter, related_name='matches_as_fighter2', on_delete=models.CASCADE)
    weight_class = models.CharField(max_length=50)
    is_main_event = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.fighter1} vs {self.fighter2} at {self.event}"

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, related_name='votes', on_delete=models.CASCADE)
    chosen_fighter = models.ForeignKey(Fighter, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'match')

    def __str__(self):
        return f"{self.user} voted for {self.chosen_fighter} in {self.match}"
    

    

