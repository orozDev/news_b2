from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from .models import News, Category, Tag, Comment

# admin.site.register(News)
# admin.site.register(Category)
# admin.site.register(Tag)


admin.site.site_header = 'News.kg'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


class NewsAdminForm(forms.ModelForm):

    content = forms.CharField(widget=CKEditorUploadingWidget(), label='Контент')

    class Meta:
        model = News
        fields = '__all__'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'date', 'author', 'is_published', 'get_image')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'content', 'description')
    list_filter = ('date', 'category', 'tags', 'author',)
    list_editable = ('is_published',)
    readonly_fields = ('get_big_image',)
    form = NewsAdminForm

    @admin.display(description='Обложка')
    def get_image(self, item):
        return mark_safe(f'<img src="{item.image.url}" width="150px">')

    @admin.display(description='Обложка')
    def get_big_image(self, item):
        return mark_safe(f'<img src="{item.image.url}" width="100%">')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'news', 'date',)
    list_display_links = ('id', 'name',)
    list_filter = ('news', 'date',)
    search_fields = ('name', 'text',)

# Register your models here.
