from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'author', 'date']
    list_filter = ('author', 'date')


admin.site.register(Post, PostAdmin)