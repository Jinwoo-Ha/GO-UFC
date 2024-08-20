from django.contrib import admin
from .models import Post, Comment, Video, Fighter, Event, Match, Vote

# 기존 모델 등록 유지
admin.site.register(Video)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Fighter)

# 새로운 모델에 대한 admin 설정 추가
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')
    list_filter = ('date',)
    search_fields = ('title', 'location')

class MatchInline(admin.TabularInline):
    model = Match
    extra = 1

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('event', 'fighter1', 'fighter2', 'weight_class', 'is_main_event')
    list_filter = ('event', 'weight_class', 'is_main_event')
    search_fields = ('fighter1__name', 'fighter2__name', 'event__title')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'match', 'chosen_fighter', 'timestamp')
    list_filter = ('match__event', 'chosen_fighter')
    search_fields = ('user__username', 'match__fighter1__name', 'match__fighter2__name')

# Event 모델에 MatchInline 추가
class EventAdminWithMatches(EventAdmin):
    inlines = [MatchInline]

admin.site.unregister(Event)
admin.site.register(Event, EventAdminWithMatches)