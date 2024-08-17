from django.contrib import admin
from .models import Post, Comment, Video, Fighter

admin.site.register(Video)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Fighter)
