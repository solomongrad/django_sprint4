from django.contrib import admin

from .models import Category, Comment, Location, Post

admin.site.empty_value_display = 'Не задано'


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'location',
        'is_published',
        'category',
        'author',
        'pub_date',
    )
    list_editable = (
        'is_published',
        'category',
    )
    search_fields = ('title',)
    list_filter = ('category', 'author',)
    list_display_links = ('title',)


class PostInLine(admin.StackedInline):
    model = Post
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = (PostInLine,)
    list_display = (
        'title',
        'description',
        'slug',
        'is_published',
    )
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_filter = ('title',)


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
    )
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_filter = ('is_published',)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'post',
        'created_at',
        'author',
    )
    search_fields = ('text',)
    list_filter = ('post',)


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Comment, CommentAdmin)
