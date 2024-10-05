from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, News, Contact, Comments

admin.site.register(Contact)


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = 'user', 'comment', 'created_at', 'active'
    list_filter = ['active', 'created_at']
    search_fields = ['user', 'comment']
    actions = ['disabled_comments', 'active_comments']

    def disabled_comments(self, request, queryset):
        queryset.update(active=False)

    def active_comments(self, request, queryset):
        queryset.update(active=True)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name'


@admin.register(News)
class NewAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'body', 'category', 'publish_time', 'status', 'show_image',
    list_filter = 'title', 'publish_time', 'status',
    prepopulated_fields = {'slug': ('title',)}

    def show_image(self, obj: News):
        return mark_safe('<img src="%s" width="150" height="150" />' % (obj.image.url))

    show_image.short_description = "Image"
