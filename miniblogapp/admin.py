from django.contrib import admin

# Register your models here.
from miniblogapp.models import Post, Comment, Profile


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_created', 'author']
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',),}

    inlines = [CommentInline]




admin.site.register(Comment)
admin.site.register(Profile)
