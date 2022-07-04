from django.contrib import admin
from django.utils.safestring import mark_safe
# Register your models here.
from .models import SubCategory, SuperCategory, Product, ExtraImage, IpCategory, IpModel, Order, About, Carousel


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 5
    readonly_fields = ('get_image', 'views')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width=80px>')
    
    get_image.short_description = 'Current image'
    

class SuperCategoryAdmin(admin.ModelAdmin):
    inlines = (SubCategoryInline,)
    search_fields = ('name',)
    list_per_page = 6
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width=80px>')
    
    get_image.short_description = 'Current image'


class ExtraImageInline(admin.TabularInline):
    model = ExtraImage
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width=80px>')
    
    get_image.short_description = 'Current image'

class ProductAdmin(admin.ModelAdmin):
    inlines = (ExtraImageInline,)
    fields = ('name', 'slug', 'category','description', 'info', 'thumbnail', 'get_thumbnail', 'price', 'views',
    'created_at', 'changed_at', 'author')
    readonly_fields = ('get_thumbnail', 'views', 'created_at', 'changed_at')
    list_display = ('name', 'category', 'price', 'get_thumbnail', 'created_at')
    list_filter = ('category',)
    prepopulated_fields = {'slug':('name',)}
    list_per_page = 6
    save_on_top = True
    save_as_continue = True
    save_as = True
    search_fields = ('author__username', 'name', 'price')


    def get_thumbnail(self, obj):
        return mark_safe(f'<img src={obj.thumbnail.url} width=80px>')
    
    get_thumbnail.short_description = 'Current thumbnail'


class CarouselInline(admin.TabularInline):
    model = Carousel
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width=80px>')
    
    get_image.short_description = 'Current image'


class AboutAdmin(admin.ModelAdmin):
    inlines = (CarouselInline, )
    list_display = ('name', 'phone', 'get_banner')
    readonly_fields = ('get_banner',)

    def get_banner(self, obj):
        return mark_safe(f'<img src={obj.banner.url} width=80px>')
    
    get_banner.short_description = 'Current banner'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'phone', 'quantity', 'date', 'status')
    fields = ('customer', 'phone', 'product', 'quantity', 'price', 'date', 'status')
    list_filter = ('status',)
    list_editable = ('status', )
    readonly_fields = ('customer', 'phone', 'product', 'quantity', 'price', 'date',)
    list_per_page = 6


admin.site.register(Product, ProductAdmin)
admin.site.register(SuperCategory, SuperCategoryAdmin)
admin.site.register(IpModel)
admin.site.register(IpCategory)
admin.site.register(Order, OrderAdmin)
admin.site.register(About, AboutAdmin)
