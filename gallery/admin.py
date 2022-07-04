from django.contrib import admin
from django.utils.safestring import mark_safe
# Register your models here.
from .models import Picture, IpModel


class PictureAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'tags', ('image', 'get_image'), 'image_type', 'views', 'author')
    list_display = ('name', 'created_at','tag_list' , 'get_image')
    readonly_fields = ('views', 'get_image')
    search_fields = ('name', 'tags__name', 'author__username')
    list_per_page = 6
    save_on_top = True
    date_hierarchy = 'created_at'

    def tag_list(self, obj):
        return u', '.join(t.name for t in obj.tags.all())
    
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width=80px>')

admin.site.register(Picture, PictureAdmin)
admin.site.register(IpModel)