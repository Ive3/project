from django.contrib import admin
from django.utils.safestring import mark_safe
# Register your models here.
from .models import Category, Post, ExtraImage, SocialName, Links, IpModel, Comment, About


class ExtraImageInlines(admin.TabularInline):
    model = ExtraImage
    readonly_fields = ('get_image',)
    
    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width=75px>')
        else:
            return 'No Image'
    get_image.short_description = 'Current image'


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'show', 'category', 'get_thumbnail', 'created')
    list_editable = ('show',)
    fields = ('title', 'slug', 'category', 'short_description', 'text',('thumbnail', 'get_thumbnail'), 'video', 'author',('created', 'changed'), ('views', 'likes'))
    readonly_fields = ('views', 'likes', 'created', 'changed', 'get_thumbnail')
    inlines = (ExtraImageInlines,)
    prepopulated_fields = {'slug':('title',)}
    list_per_page = 6
    list_filter = ('category', 'show')
    search_fields = ['title', 'author__username']
    save_on_top = True
    save_as = True
    save_as_continue = True

    def get_thumbnail(self, obj):
        if obj.thumbnail:
            return mark_safe(f'<img src="{obj.thumbnail.url}" width=75px>')
        else:
            return 'No Image'
    get_thumbnail.short_description = 'Current thumbnail'
        

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_img')
    fields = ('name', 'slug', ('image', 'get_img'))
    readonly_fields = ('get_img',)
    prepopulated_fields = {'slug':('name',)}
    search_fields = ('name', 'author__username')


    def get_img(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="75px">')
        else:
            return 'No Image'
    get_img.short_description = 'Current image'


class LinksInlines(admin.TabularInline):
    model = Links


class SocialnameInlines(admin.ModelAdmin):
    inlines = (LinksInlines,)
    search_fields = ('name', 'author__username')



class AboutAdmin(admin.ModelAdmin):
    list_display = ('get_image', 'active')
    list_editable = ('active',)
    fields = ('description', 'get_image', 'image', 'video', 'active')
    readonly_fields = ('get_image',)
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width=80px>')
    
    get_image.short_description = 'Current image'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    search_fields = ('name', 'author__username', 'post')



admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(SocialName, SocialnameInlines)
admin.site.register(IpModel)
admin.site.register(Comment, CommentAdmin)
admin.site.register(About, AboutAdmin)
