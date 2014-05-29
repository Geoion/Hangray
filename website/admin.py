from django.contrib import admin
from website import models

#todo change the admin form


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('account', 'city', 'industry', 'register_time')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'time', 'account')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('author', 'question', 'content', 'time')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'answer', 'content', 'time')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'follow_by', 'time')


class EventAdmin(admin.ModelAdmin):
    list_display = ('account', 'question', 'answer', 'time')


admin.site.register(models.UserInfo, UserInfoAdmin)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Answer, AnswerAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Follow, FollowAdmin)
admin.site.register(models.Event, EventAdmin)